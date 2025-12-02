import os
import psycopg2
import pandas as pd

df = pd.read_csv('data/processed/reviews_processed.csv')


conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
cur = conn.cursor()

# Insert banks and get their IDs
banks = df['bank'].unique()
bank_id_map = {}
for bank in banks:
    cur.execute("INSERT INTO banks (bank_name, app_name) VALUES (%s, %s) ON CONFLICT (bank_name) DO NOTHING RETURNING bank_id;", (bank, bank + " Mobile"))
    result = cur.fetchone()
    if result:
        bank_id_map[bank] = result[0]
    else:
        # fetch existing bank_id if insert skipped
        cur.execute("SELECT bank_id FROM banks WHERE bank_name = %s;", (bank,))
        bank_id_map[bank] = cur.fetchone()[0]

# Insert reviews
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            bank_id_map[row['bank']],
            row['review'],
            row['rating'],
            row['date'],
            row.get('sentiment_label', None),
            row.get('sentiment_score', None),
            row.get('source', 'Google Play')
        )
    )

conn.commit()
cur.close()
conn.close()
