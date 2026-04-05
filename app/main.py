from fastapi import FastAPI

app = FastAPI(title="FastAPI CI Demo")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello from FastAPI CI demo"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}