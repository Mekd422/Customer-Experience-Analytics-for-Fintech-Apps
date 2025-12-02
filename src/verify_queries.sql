SELECT COUNT(*) AS total_reviews FROM reviews;

-- Count reviews per bank
SELECT b.bank_name, COUNT(r.review_id) AS review_count
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY review_count DESC;

-- Average rating per bank
SELECT b.bank_name, AVG(r.rating) AS average_rating
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY average_rating DESC;

-- Sentiment distribution per bank
SELECT b.bank_name, r.sentiment_label, COUNT(*) AS count
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name, r.sentiment_label
ORDER BY b.bank_name, count DESC;

-- Check for nulls or missing sentiment labels
SELECT COUNT(*) AS missing_sentiment FROM reviews WHERE sentiment_label IS NULL;

-- Sample 5 reviews per bank to manually verify
SELECT b.bank_name, r.review_text, r.rating, r.sentiment_label
FROM banks b
JOIN reviews r ON b.bank_id = r.bank_id
ORDER BY RANDOM()
LIMIT 15;
