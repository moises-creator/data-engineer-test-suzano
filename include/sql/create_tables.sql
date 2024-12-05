CREATE TABLE IF NOT EXISTS Bloomberg_Commodity_Index (
    date DATE NOT NULL,
    close DECIMAL(10, 2),
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    volume BIGINT,
    PRIMARY KEY (date)
);

CREATE TABLE IF NOT EXISTS usd_cny (
    date DATE NOT NULL,
    close DECIMAL(10, 2),
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    volume BIGINT,
    PRIMARY KEY (date)
);

CREATE TABLE IF NOT EXISTS chinese_caixin_services_index (
    date DATE NOT NULL,
    actual_state VARCHAR(255),
    close DECIMAL(10, 2),
    forecast DECIMAL(10, 2),
    PRIMARY KEY (date)
);
