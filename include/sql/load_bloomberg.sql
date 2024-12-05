INSERT INTO Bloomberg_Commodity_Index (date, close, open, high, low, volume)
VALUES (%(date)s, %(close)s, %(open)s, %(high)s, %(low)s, %(volume)s)
ON CONFLICT (date) DO NOTHING;
