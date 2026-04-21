from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.cache import check_redis, redis_client
from app.config import settings
from app.db import check_db, get_db, init_db
from app.models import Click, ShortUrl
from app.schemas import ShortenRequest, ShortenResponse, StatsResponse
from app.shortener import generate_short_code


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Lifespan function to initialize resources on startup."""
    init_db()  # Initialize the database
    yield  # Run the application


app = FastAPI(title="URL Shortener API", description="A simple URL shortener API built with FastAPI", version="1.0.0", lifespan=lifespan)


@app.get("/health", tags=["Health Check"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", tags=["Health Check"])
def ready() -> dict[str, object]:
    checks = {"db": check_db(), "redis": check_redis()}
    if not all(checks.values()):
        raise HTTPException(status_code=503, detail={"status": "not_ready", "checks": checks})
    return {"status": "ready", "checks": checks}


@app.post("/api/shorten", response_model=ShortenResponse, tags=["URL Shortening"], status_code=201)
def shorten(payload: ShortenRequest, request: Request, db: Session = Depends(get_db)) -> ShortenResponse:
    original = str(payload.url)

    # Try until 5 times if have a collision (extremely improbable with 62^6 combinations)
    for _ in range(5):
        short_code = generate_short_code()
        existing = db.query(ShortUrl).filter_by(short_code=short_code).first()
        if not existing:
            break
    else:
        raise HTTPException(status_code=500, detail="Could not generate a unique short code after 5 attempts")

    record = ShortUrl(short_code=short_code, original_url=original)
    db.add(record)
    db.commit()
    db.refresh(record)

    # Populate cache
    redis_client.setex(f"url:{short_code}", settings.cache_ttl_seconds, original)

    base = str(request.base_url).rstrip("/")
    return ShortenResponse(
        short_code=short_code,
        short_url=f"{base}/{short_code}",
        original_url=original,
    )


@app.get("/{short_code}", tags=["Redirection"])
def redirect(short_code: str, request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    # Reserve routes that not are short codes
    if short_code in ("health", "ready", "docs", "openapi.json", "redoc"):
        raise HTTPException(status_code=404)
    
    # Check cache first
    original = redis_client.get(f"url:{short_code}")

    record = db.query(ShortUrl).filter_by(short_code=short_code).first()
    if not record:
        raise HTTPException(status_code=404, detail="Short code not found")
    
    if not original:
        original = record.original_url
        redis_client.setex(f"url:{short_code}", settings.cache_ttl_seconds, original)

    # Log click
    click = Click(
        short_url_id=record.id,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(click)
    db.commit()

    return RedirectResponse(url=original, status_code=301)


@app.get("/api/stats/{short_code}", response_model=StatsResponse, tags=["Statistics"])
def stats(short_code: str, db: Session = Depends(get_db)) -> StatsResponse:
    record = db.query(ShortUrl).filter_by(short_code=short_code).first()
    if not record:
        raise HTTPException(status_code=404, detail="Short code not found")
    
    last_click = (
        db.query(Click)
        .filter_by(short_url_id=record.id)
        .order_by(Click.clicked_at.desc())
        .first()
    )

    return StatsResponse(
        short_code=record.short_code,
        original_url=record.original_url,
        total_clicks=len(record.clicks),
        created_at=record.created_at,
        last_click_at=last_click.clicked_at if last_click else None,
    )