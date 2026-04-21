from fastapi import FastAPI

app = FastAPI(title="URL Shortener API", description="A simple URL shortener API built with FastAPI", version="1.0.0")

@app.get("/health", tags=["Health Check"])
def health():
    return {"status": "ok"}

@app.get("/ready", tags=["Health Check"])
def ready():
    return {"status": "ready", "checks": {"db": True, "redis": True}}
