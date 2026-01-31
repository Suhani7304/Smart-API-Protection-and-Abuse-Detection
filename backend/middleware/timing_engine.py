import statistics
from fastapi import Request
from sqlalchemy.orm import Session
from database import SessionLocal
from models.timing_metrics import TimingMetrics
from models.models_session import SessionActivity
import time
from middleware.risk_aggregator import add_risk

FAST_ACTION_THRESHOLD_MS = 300
LOW_VARIANCE_THRESHOLD = 50

def analyze_timing(deltas: list[float]) -> int:
    risk = 0
    if not deltas:
        return risk 

    if deltas[-1] < FAST_ACTION_THRESHOLD_MS:
        risk += 20

    if len(deltas) >= 3:
        variance = statistics.pvariance(deltas)
        if variance < LOW_VARIANCE_THRESHOLD:
            risk += 15
    
    if len(deltas)>=4 and sum(deltas)<8000:
        risk += 30

    return risk

async def timing_engine_middleware(request: Request, call_next):
    response = await call_next(request)
    session_id = request.cookies.get("session_id")
    ip = request.client.host if request.client else "unknown"
    if not session_id:
        return response
    
    db: Session = SessionLocal()
    actions = (
        db.query(SessionActivity)
        .filter(SessionActivity.session_id == session_id)
        .order_by(SessionActivity.timestamp.desc())
        .limit(5)
        .all()
    )
    if len(actions)<2:
        db.close()
        return response

    deltas = []
    for i in range(len(actions)-1):
        delta = (actions[i].timestamp - actions[i+1].timestamp).total_seconds()*1000
        deltas.append(abs(delta))

    risk = analyze_timing(deltas)

    if risk>0:
        add_risk(
            session_id=session_id,
            ip=ip,
            points=risk
        )

    metric = TimingMetrics(
        session_id=session_id,
        action=actions[0].action,
        delta_ms=deltas[0],
        risk_score=risk
    )

    db.add(metric)
    db.commit()
    db.close()

    return response