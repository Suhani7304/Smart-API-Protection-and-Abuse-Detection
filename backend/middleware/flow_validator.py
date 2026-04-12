from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models_session import SessionActivity
from middleware.risk_aggregator import add_risk

FLOW_ORDER = ["/", "search", "select", "confirm", "pay"]
FLOW_INDEX = {action: i for i, action in enumerate(FLOW_ORDER)}

SAFE_ENDPOINTS = {"/","/favicon.ico", "/docs", "/redoc", "/openapi.json"}

def get_action_from_path(path: str):
    if path == "/":
        return "/"
    if path == "/search":
        return "search"
    if path == "/select-seat":
        return "select"
    if path == "/confirm":
        return "confirm"
    if path == "/pay":
        return "pay"
    return None

async def flow_validator_middleware(request: Request, call_next):
    path = request.url.path

    if path in SAFE_ENDPOINTS:
        return await call_next(request)

    action = get_action_from_path(path)
    if not action:
        return await call_next(request)

    session_id = request.cookies.get("session_id")
    if not session_id:
        return JSONResponse(
            status_code=400,
            content={"detail": "Session missing"}
        )

    db: Session = SessionLocal()

    last = (
        db.query(SessionActivity)
        .filter(SessionActivity.session_id == session_id)
        .order_by(SessionActivity.timestamp.desc())
        .first()
    )

    if last:
        prev_idx = FLOW_INDEX.get(last.action, -1)
        curr_idx = FLOW_INDEX.get(action, -1)

        #refresh
        if curr_idx == prev_idx:
            pass

        #backward navigation
        elif curr_idx < prev_idx:
            pass

        # Jumping bw pages
        elif curr_idx - prev_idx > 1:
            add_risk(
                session_id=session_id,
                ip=request.client.host,
                points=40
            )

    db.add(SessionActivity(
        session_id=session_id,
        ip_address=request.client.host if request.client else None,
        action=action
    ))
    db.commit()
    db.close()

    return await call_next(request)
