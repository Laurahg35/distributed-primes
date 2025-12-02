CREATE TABLE IF NOT EXISTS primes (
  id SERIAL PRIMARY KEY,
  request_id VARCHAR(64) NOT NULL,
  prime TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(request_id, prime)
);
