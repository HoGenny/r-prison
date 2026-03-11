# Backend Lint & Format Guide
*Python* 최신 표준을 유지하고, 6명의 코드 스타일을 하나로 통일하기 위해 *Ruff*를 사용합니다.

## ✅ 필수 설정

### Ruff 설치
```Bash
pip install ruff
```
##  🛠 명령어
- VS Code 익스텐션 마켓에서 'Ruff' 설치
- 익스텐션을 설치했다면 저장(Ctrl+S) 시 자동으로 수정되지만, 수동으로 확인하려면 아래 명령어를 사용합니다.

에러 체크 및 자동 수정
```bash
ruff check --fix .
```
- 코드 스타일 교정
```bash
 ruff format .
```

## 📋 우리 팀 주요 규칙
- *Line Length* : 최대 100자 허용.
- *Quotes* : 모든 문자열은 큰따옴표(") 사용.
- *Import* 위치 : from __future__ import annotations는 반드시 파일 최상단에 위치 (Ruff가 자동 교정).