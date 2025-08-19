param(
    [string]$RepoName = "",
    [string]$RemoteUrl = "",
    [switch]$Private
)

function Ensure-Command {
    param([string]$Name)
    $null = & $Name --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        return $false
    }
    return $true
}

Write-Host "=== GitHub Upload Helper ===" -ForegroundColor Cyan

# 1) Check git
if (-not (Ensure-Command git)) {
    Write-Error "Git is not installed or not in PATH. Install Git from https://git-scm.com/downloads and try again."
    exit 1
}

# 2) Create .gitignore if missing (safety)
$gitignore = Join-Path $PSScriptRoot "..\.gitignore"
if (-not (Test-Path $gitignore)) {
    @(
        "__pycache__/",
        "*.py[cod]",
        "venv/",
        ".venv/",
        ".idea/",
        ".vscode/",
        "media/",
        "*.sqlite3"
    ) | Set-Content -Path $gitignore -Encoding UTF8
    Write-Host ".gitignore created." -ForegroundColor Yellow
}

Push-Location (Join-Path $PSScriptRoot "..")
try {
    # 3) Initialize git repo if needed
    $inside = & git rev-parse --is-inside-work-tree 2>$null
    if ($LASTEXITCODE -ne 0) {
        git init | Out-Null
        Write-Host "Initialized empty Git repository." -ForegroundColor Green
    }

    # 4) Set default branch to main
    git symbolic-ref --short HEAD 1>$null 2>$null
    if ($LASTEXITCODE -ne 0) {
        git checkout -b main 1>$null
        Write-Host "Created main branch." -ForegroundColor Green
    } else {
        $currentBranch = git branch --show-current
        if ($currentBranch -ne "main") {
            git branch -M main 1>$null
            Write-Host "Switched default branch to main." -ForegroundColor Green
        }
    }

    # 5) Stage and commit if nothing committed yet or there are changes
    $hasCommit = git rev-parse HEAD 2>$null
    git add -A
    $status = git status --porcelain
    if (-not [string]::IsNullOrWhiteSpace($status)) {
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($hasCommit)) {
            git commit -m "Initial commit" | Out-Null
            Write-Host "Created initial commit." -ForegroundColor Green
        } else {
            git commit -m "Update" | Out-Null
            Write-Host "Committed changes." -ForegroundColor Green
        }
    } else {
        Write-Host "No changes to commit." -ForegroundColor DarkGray
    }

    # 6) Configure remote
    $originUrl = git remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0) {
        if ([string]::IsNullOrWhiteSpace($RemoteUrl)) {
            # Try to create GitHub repo via gh if available
            $ghAvailable = Ensure-Command gh
            if ($ghAvailable) {
                if ([string]::IsNullOrWhiteSpace($RepoName)) {
                    $RepoName = Split-Path -Leaf (Get-Location).Path
                    Write-Host "Using folder name as repository name: $RepoName" -ForegroundColor Yellow
                }
                $visibility = if ($Private.IsPresent) { "private" } else { "public" }
                Write-Host "Creating GitHub repository '$RepoName' ($visibility) via GitHub CLI..." -ForegroundColor Cyan
                gh repo create $RepoName --$visibility --source . --remote origin --push
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "Repository created and pushed successfully via gh." -ForegroundColor Green
                    exit 0
                } else {
                    Write-Warning "gh failed to create/push repository. You can pass -RemoteUrl or login with 'gh auth login'."
                }
            } else {
                Write-Warning "GitHub CLI (gh) not found. Install from https://cli.github.com/ or provide -RemoteUrl."
            }
            Write-Error "No remote configured. Re-run with -RemoteUrl 'https://github.com/<user>/<repo>.git' or install/login to GitHub CLI and re-run."
            exit 1
        } else {
            git remote add origin $RemoteUrl
            Write-Host "Added remote origin: $RemoteUrl" -ForegroundColor Green
        }
    } else {
        Write-Host "Remote origin already set: $originUrl" -ForegroundColor DarkGray
    }

    # 7) Push to origin
    Write-Host "Pushing to origin main..." -ForegroundColor Cyan
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Pushed successfully!" -ForegroundColor Green
    } else {
        Write-Error "Push failed. Ensure you have permission and correct credentials. Consider using 'gh auth login'."
        exit 1
    }
}
finally {
    Pop-Location
}
