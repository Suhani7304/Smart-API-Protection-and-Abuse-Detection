from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models_session import SessionActivity

VALID_FLOW = {
    "search": ["select"],
    "select": ["confirm"],
    "confirm": ["pay"],
    "pay": []
}

def get_action_from_path(path: str):
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
    action = get_action_from_path(request.url.path)

    if not action:
        return await call_next(request)

    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="Session missing")

    db: Session = SessionLocal()

    last = (
        db.query(SessionActivity)
        .filter(SessionActivity.session_id == session_id)
        .order_by(SessionActivity.timestamp.desc())
        .first()
    )

    if last:
        allowed = VALID_FLOW.get(last.action, [])
        if action not in allowed:
            db.close()
            raise HTTPException(
                status_code=403,
                detail="Invalid booking flow detected"
            )

    db.add(SessionActivity(
        session_id=session_id,
        ip_address=request.client.host,
        action=action
    ))
    db.commit()
    db.close()

    return await call_next(request)
