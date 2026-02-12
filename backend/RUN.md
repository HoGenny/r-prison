# Run Guide

## 0) Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## 1) Copy env
```bash
cp .env.example .env
```
`DATABASE_URL` default is `postgresql+asyncpg://app:app@localhost:5433/app`.

## 2) Start PostgreSQL
```bash
docker compose up -d db
```

## 3) Apply migration
```bash
alembic upgrade head
```

## 4) Start API server
```bash
uvicorn app.main:app --reload
```

## 5) Health check
```bash
curl localhost:8000/health
```

## 6) Catalog API checks
```bash
curl localhost:8000/gacha/boxes
curl localhost:8000/slimes
```

## Optional: autogenerate migration
```bash
alembic revision --autogenerate -m "init"
```
