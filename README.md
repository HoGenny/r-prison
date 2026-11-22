# R-Prison

할 일(To-Do)을 완료하면 보상 포인트(RP)를 얻고, 그 RP로 슬라임을 뽑고·부화시키고·키우는 **게임형 투두 앱**입니다.

> 🚧 개발 중인 팀 프로젝트입니다. 백엔드 API 뼈대와 DB 모델이 잡혀 있고, 일부 서비스 로직과 프론트엔드는 구현 전입니다.

## 주요 기능 (설계 기준)

- **투두 & 캘린더**: 날짜별 할 일 등록, 완료/완료 취소, 난이도·카테고리별 보상 RP
- **RP 원장**: RP 지급·회수 내역을 트랜잭션 로그로 기록
- **뽑기(Gacha)**: RP로 뽑기 상자를 열어 등급별 확률로 슬라임 획득
- **부화(Incubation)**: 슬라임 알을 일정 기간 부화
- **슬라임 육성**: 레벨·경험치·호감도
- **아이템 & 업적**

## 기술 스택

| 구분 | 스택 |
| --- | --- |
| Backend | Python 3.11, FastAPI, SQLAlchemy 2 (async), Alembic, PostgreSQL, JWT |
| Frontend | React 19, Vite |
| 품질 | Ruff (lint·format), pytest |

## 구조

```
.
├── backend/
│   ├── app/
│   │   ├── api/v1/     # 라우터 (auth, users, todos, calendar, slimes, incubations, gacha, items, achievements)
│   │   ├── models/     # SQLAlchemy 모델
│   │   ├── schemas/    # Pydantic 스키마
│   │   ├── services/   # 비즈니스 로직
│   │   └── core/       # 설정, DB, 보안, 에러 처리
│   ├── migrations/     # Alembic
│   └── tests/
├── frontend/           # React + Vite
└── docs/               # 코드 리뷰 가이드, 커밋 메시지 예시
```

## 실행 방법

- 백엔드: [backend/RUN.md](./backend/RUN.md) 참고 (Docker로 PostgreSQL 실행 → `alembic upgrade head` → `uvicorn app.main:app --reload`)
- 프론트엔드:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

---

## Git 협업 규칙

> 자세한 규칙은 [CONTRIBUTING.md](./.github/CONTRIBUTING.md), [코드 리뷰 가이드](./docs/CODE_REVIEW_GUIDE.md), [커밋 메시지 예시](./docs/COMMIT_MESSAGE_EXAMPLES.md)를 참고하세요.

### 브랜치 정책
- main 브랜치에는 직접 push 하지 않습니다.
- 모든 작업은 `feature/기능이름` 브랜치에서 수행합니다.
- 작업 완료 후 PR 생성 → 리뷰 승인 후 Merge 합니다.

### 커밋 메시지 예시
- `Feat: 로그인 API 요청 기능 추가`
- `Fix: 토큰 응답값 null 처리 로직 수정`
- `Docs: API 엔드포인트 목록 업데이트`

### PR 규칙
- PR 하나는 목적 하나(기능 하나)
- 최소 1명 승인 후 Merge
- Squash and merge 권장

### PR 전 체크리스트 (Backend)
1. [ ] 로컬에서 `ruff check .` 실행 시 에러가 없는가?
2. [ ] 모든 파일에 대해 `ruff format .`이 적용되었는가?
3. [ ] 사용하지 않는 모듈(`import`)이 깨끗하게 정리되었는가?
