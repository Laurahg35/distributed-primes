from fastapi import FastAPI
import psycopg2, os, psycopg2.extras

app = FastAPI()

DB_URL = os.environ.get("DATABASE_URL")

def conn():
    return psycopg2.connect(DB_URL)

@app.get("/status/{request_id}")
def status(request_id: str):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT COUNT(*) FROM primes WHERE request_id=%s;", (request_id,))
    count = cur.fetchone()[0]
    cur.close()
    c.close()

    return {"request_id": request_id, "generated": count}
