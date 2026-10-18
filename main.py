import time
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Startup time for uptime calculation
START_TIME = time.time()

# Prometheus Counter
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

# In-memory log storage
log_entries = []

@app.middleware("http")
async def log_requests(request: Request, call_next):
    REQUEST_COUNT.inc()
    request_id = str(uuid.uuid4())
    path = request.url.path
    
    # Log entry format
    log_entry = {
        "level": "INFO",
        "ts": time.time(),
        "path": path,
        "request_id": request_id
    }
    log_entries.append(log_entry)
    
    response = await call_next(request)
    return response

@app.get("/work")
def do_work(n: int = 1, email: str = "24f2006714@ds.study.iitm.ac.in"):
    # Do K units of work (simulation)
    total = 0
    for i in range(n * 1000):
        total += i
    return {"email": email, "done": n}

@app.get("/metrics")
def metrics():
    data = generate_latest(REQUEST_COUNT)
    return JSONResponse(
        content=data.decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/healthz")
def healthz():
    uptime = time.time() - START_TIME
    return {"status": "ok", "uptime_s": uptime}

@app.get("/logs/tail")
def logs_tail(limit: int = 10):
    # Return the last N log entries
    return log_entries[-limit:]