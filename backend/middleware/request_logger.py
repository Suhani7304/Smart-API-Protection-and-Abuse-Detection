import time
from fastapi import Request
from sqlalchemy.orm import Session
from database import SessionLocal
from models.request_log import APIRequestLog

IGNORED_PATHS = {
    "/favicon.ico",
    "/docs",
    "/redoc",
    "/openapi.json"
}

async def request_logger_middleware(request: Request, call_next):

    if request.url.path in IGNORED_PATHS:
        return await call_next(request)
        
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    db: Session = SessionLocal()
    try:
        log = APIRequestLog(
            ip_address=request.client.host if request.client else None,
            method=request.method,
            endpoint=request.url.path,
            user_agent=request.headers.get("user-agent"),
            api_key=request.headers.get("x-api-key"),
            session_id=request.cookies.get("session_id"),
            status_code=response.status_code,
            response_time_ms=process_time
        )
        db.add(log)
        db.commit()
    finally:
        db.close()

    return response
