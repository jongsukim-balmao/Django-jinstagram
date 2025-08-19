\# django jinstagram clone coding 



\## 실행

&nbsp;python



---

## GitHub 업로드 방법 (Windows / PowerShell)
이 프로젝트를 내 GitHub 저장소로 올리기 위한 스크립트를 포함했습니다.

사전 준비물:
- Git 설치: https://git-scm.com/downloads
- (선택) GitHub CLI 설치 및 로그인: https://cli.github.com/  → `gh auth login`

스크립트 위치:
- `scripts/push_to_github.ps1`

사용 방법 1: GitHub CLI(gh) 사용해 자동으로 원격 저장소 생성 + 푸시
1) PowerShell을 프로젝트 루트에서 실행
2) `gh auth login`으로 GitHub 로그인 (최초 1회)
3) 실행
   - 공개 저장소: `powershell -ExecutionPolicy Bypass -File .\scripts\push_to_github.ps1 -RepoName "원하는_레포_이름"`
   - 비공개 저장소: `powershell -ExecutionPolicy Bypass -File .\scripts\push_to_github.ps1 -RepoName "원하는_레포_이름" -Private`

사용 방법 2: 이미 GitHub에 빈 저장소를 만들어두었을 때
1) GitHub에서 https://github.com/new 로 저장소 생성 (예: https://github.com/USER/REPO.git)
2) PowerShell에서 실행
   - `powershell -ExecutionPolicy Bypass -File .\scripts\push_to_github.ps1 -RemoteUrl "https://github.com/USER/REPO.git"`

스크립트가 하는 일:
- Git 설치 확인 후, 현재 폴더를 Git 저장소로 초기화 (필요 시)
- 기본 브랜치를 main으로 설정
- 변경사항 커밋 (필요 시)
- 원격 origin이 없으면 추가하거나, gh로 GitHub 저장소 생성
- `main` 브랜치 푸시

주의 사항:
- `.gitignore`가 포함되어 있어 다음 파일/폴더는 업로드에서 제외됩니다: `__pycache__/`, `*.sqlite3`, `media/`, `venv/`, `.venv/`, `.idea/`, `.vscode/` 등.
- SQLite DB와 media 폴더는 개인 데이터가 있을 수 있으니 업로드 대상에서 제외하는 것이 일반적입니다.
