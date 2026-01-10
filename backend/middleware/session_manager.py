import uuid
from fastapi import Request, Response

SESSION_COOKIE = "session_id"

async def session_middleware(request: Request, call_next):
    response: Response

    session_id = request.cookies.get(SESSION_COOKIE)

    response = await call_next(request)

    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key=SESSION_COOKIE,
            value=session_id,
            httponly=True,
            max_age=1800,  # 30 minutes
            samesite="lax"
        )

    return response
                