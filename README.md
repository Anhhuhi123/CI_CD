# FastAPI CI Demo (Minimal)

Repo demo toi gian de hoc va test CI voi GitHub Actions.

## 1) Chay local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Kiem tra endpoint:

- `GET http://localhost:8000/`
- `GET http://localhost:8000/health`

## 2) Chay test local

```bash
source .venv/bin/activate
pytest
ruff check .
```

## 3) CI trigger hoat dong nhu the nao

Workflow nam tai `.github/workflows/ci.yml` va chi chay khi co **pull_request vao branch `dev-v2`**.

Pipeline se:

1. Checkout code
2. Setup Python 3.11
3. Install dependencies (`requirements.txt`) va cai them `ruff`, `pytest`
4. Chay `ruff check .`
5. Chay `pytest`
6. Chay `docker build` de verify Dockerfile

Neu bat ky buoc nao fail thi job CI fail.

## 4) Cach tao PR vao dev-v2 de thay CI chay

```bash
git checkout -b feature/test-ci
git add .
git commit -m "Add minimal FastAPI CI demo"
git push origin feature/test-ci
```

Sau do len GitHub:

1. Mo Pull Request
2. Base branch chon `dev-v2`
3. Compare branch chon `feature/test-ci`
4. Tao PR va vao tab Actions/Checks de xem CI

## 5) Chay bang Docker

```bash
docker build -t fastapi-ci-demo:local .
docker run --rm -p 8000:8000 fastapi-ci-demo:local
```

abc