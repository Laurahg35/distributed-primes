from fastapi import FastAPI, HTTPException
import uuid, json, os, redis

app = FastAPI()

REDIS_URL = os.environ.get("REDIS_URL")
r = redis.from_url(REDIS_URL)

@app.post("/new")
def create_task(count: int, digits: int):
    if count <= 0 or digits < 12:
        raise HTTPException(status_code=400, detail="count>0 and digits>=12")

    request_id = str(uuid.uuid4())
    task = {"id": request_id, "count": count, "digits": digits}

    r.rpush("prime_tasks", json.dumps(task))

    return {"request_id": request_id}
