# DjangoProject_jinstagram/settings.py

# 1. 공통 설정(settings_base.py)을 모두 가져옵니다.
from .settings_base import *

# 2. 환경별 설정(local_settings.py)이 있다면 덮어씁니다.
try:
    from .local_settings import *
except ImportError:
    pass