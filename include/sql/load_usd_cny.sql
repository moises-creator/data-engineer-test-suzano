INSERT INTO usd_cny (date, close, open, high, low, volume)
VALUES (%(date)s, %(close)s, %(open)s, %(high)s, %(low)s, %(volume)s)
ON CONFLICT (date) DO NOTHING;
