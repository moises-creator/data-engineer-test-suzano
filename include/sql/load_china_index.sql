INSERT INTO chinese_caixin_services_index (date, actual_state, close, forecast)
VALUES (%(date)s, %(actual_state)s, %(close)s, %(forecast)s)
ON CONFLICT (date) DO NOTHING;
