# 로컬 실행 가이드

## 사전 준비

- Python 3.11+
- Docker & Docker Compose

## 1. 가상환경 & 의존성 설치

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e ".[dev]"
```

## 2. 환경 변수 설정

```bash
cp .env.example .env
```

> `.env.example` 그대로 사용하면 로컬 Docker PostgreSQL에 연결됩니다.
> Supabase 등 외부 DB를 쓸 경우 `DATABASE_URL`만 변경하세요.
> **주의**: 로컬 사용 시, `DATABASE_URL`은 반드시 `postgresql+asyncpg://` 스킴을 사용해야 합니다.

## 3. PostgreSQL 실행

```bash
docker compose up -d db
```

컨테이너 상태 확인:

```bash
docker compose ps        # STATUS가 healthy인지 확인
docker compose logs db   # 문제 시 로그 확인
```

## 4. 마이그레이션 적용

```bash
alembic upgrade head
```

## 5. API 서버 실행

```bash
uvicorn app.main:app --reload
```

## 6. 헬스 체크

```bash
curl http://localhost:8000/health
# {"ok": true}
```

API 문서: http://localhost:8000/docs

---

## 유용한 명령어

```bash
# 마이그레이션 자동 생성 (모델 변경 후)
alembic revision --autogenerate -m "설명"

# DB 초기화 (데이터 삭제 후 재생성)
alembic downgrade base
alembic upgrade head

# 테스트 실행
pytest

# DB 컨테이너 중지 / 데이터 포함 삭제
docker compose down
docker compose down -v   # 볼륨(데이터)까지 삭제
```