CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) UNIQUE NOT NULL,
    app_name VARCHAR(255) NOT NULL
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INT NOT NULL,
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    source VARCHAR(100)
);
