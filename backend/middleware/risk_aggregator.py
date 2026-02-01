from sqlalchemy.orm import Session
from database import SessionLocal
from models.session_risk import SessionRisk

def add_risk(session_id: str, ip: str, points: int):
    db: Session = SessionLocal()

    risk = db.query(SessionRisk).filter_by(session_id=session_id).first()

    if not risk:
        risk = SessionRisk(
            session_id=session_id,
            ip_address=ip,
            risk_score=points
        )
        db.add(risk)
    else:
        risk.risk_score += points
    
    db.commit()
    db.close()