from fastapi import FastAPI
import psycopg2, os, psycopg2.extras

app = FastAPI()

DB_URL = os.environ.get("DATABASE_URL")

def conn():
    return psycopg2.connect(DB_URL)

@app.get("/result/{request_id}")
def result(request_id: str):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT prime FROM primes WHERE request_id=%s ORDER BY id;", (request_id,))
    rows = cur.fetchall()
    cur.close()
    c.close()

    return {
        "request_id": request_id,
        "primes": [row[0] for row in rows]
    }
