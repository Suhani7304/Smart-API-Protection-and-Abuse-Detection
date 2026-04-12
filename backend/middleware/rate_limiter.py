import time
from fastapi import Request, HTTPException
from collections import defaultdict, deque
from fastapi.responses import JSONResponse
from middleware.risk_aggregator import add_risk

# { (ip,endpoint): dequeu([timestamp])}
request_store = defaultdict(deque) 

RATE_LIMITS = {
    "/health" : {"max_requests":30, "window": 60},
    "/book-ticket" : {"max_requests":5, "window":10}
}

IGNORED_PATHS = {
    "/favicon.ico", "/docs", "/redoc", "/openapi.json"
}

async def rate_limiter_middleware(request: Request, call_next):
    path = request.url.path
    if path in IGNORED_PATHS:
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    rule = RATE_LIMITS.get(path, {"max_requests":20, "window":60})
    max_requests = rule["max_requests"]
    window = rule["window"]

    now = time.time()
    key = (client_ip, path)
    timestamps = request_store[key]
    while timestamps and now-timestamps[0]>window:
        timestamps.popleft()

    if len(timestamps) >= max_requests:
        add_risk(
            session_id=request.cookies.get("session_id"),
            ip=client_ip,
            points=25
        )
    timestamps.append(now)
    response = await call_next(request)
    return response

