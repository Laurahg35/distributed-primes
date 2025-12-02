import os, json, redis, psycopg2, random

REDIS_URL = os.environ.get("REDIS_URL")
DB_URL = os.environ.get("DATABASE_URL")

r = redis.from_url(REDIS_URL)

def get_conn():
    return psycopg2.connect(DB_URL)

# Miller-Rabin determinista para < 2^64
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]

    def check(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    for a in bases:
        if a % n == 0:
            continue
        if not check(a):
            return False
    return True

def random_candidate(digits):
    start = 10**(digits-1)
    end = 10**digits - 1
    return random.randrange(start | 1, end, 2)

def save_prime(request_id, p):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO primes (request_id, prime) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
        (request_id, str(p))
    )

    conn.commit()
    cur.close()
    conn.close()

def worker_loop():
    while True:
        _, raw = r.blpop("prime_tasks")
        task = json.loads(raw)

        request_id = task["id"]
        count = task["count"]
        digits = task["digits"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM primes WHERE request_id=%s", (request_id,))
        current = cur.fetchone()[0]
        cur.close()
        conn.close()

        while current < count:
            cand = random_candidate(digits)
            if is_prime(cand):
                save_prime(request_id, cand)
                current += 1

if __name__ == "__main__":
    worker_loop()
