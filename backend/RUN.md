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

## 2) Start PostgreSQL
```bash
docker compose up -d db
```

## 3) Apply migrations
```bash
alembic upgrade head
```

## 4) Start API
```bash
uvicorn app.main:app --reload
```

## 5) Health check
```bash
curl localhost:8000/health
```

## Optional: create a new migration
```bash
alembic revision --autogenerate -m "init"
```
