from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models.session_risk import SessionRisk
import asyncio


HARD_LIMIT = 50
BLOCK_LIMIT = 100

async def response_engine_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")

    if not session_id:
        return await call_next(request)
    
    db: Session = SessionLocal()
    risk = (
        db.query(SessionRisk)
        .filter(SessionRisk.session_id == session_id)
        .first()
    )
    db.close()

    if not risk:
        return await call_next(request)
      
    score = risk.risk_score

    if score >= BLOCK_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail":"Too many suspicious actions detected"}
        )
    
    if score >= HARD_LIMIT:
        await asyncio.sleep(2)

    return await call_next(request)