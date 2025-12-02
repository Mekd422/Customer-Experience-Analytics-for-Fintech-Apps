import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()

def get_reviews_df():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    query = """
    SELECT b.bank_name, r.review_text, r.rating, r.sentiment_label, r.sentiment_score
    FROM reviews r
    JOIN banks b ON r.bank_id = b.bank_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def plot_rating_distribution(df):
    plt.figure(figsize=(8,6))
    sns.countplot(data=df, x='rating', hue='bank_name')
    plt.title('Rating Distribution by Bank')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.legend(title='Bank')
    plt.savefig('outputs/figures/rating_distribution.png')
    plt.show()

def plot_sentiment_distribution(df):
    plt.figure(figsize=(8,6))
    sns.countplot(data=df, x='sentiment_label', hue='bank_name', order=['positive', 'neutral', 'negative'])
    plt.title('Sentiment Distribution by Bank')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.legend(title='Bank')
    plt.savefig('outputs/figures/sentiment_distribution.png')
    plt.show()

def main():
    df = get_reviews_df()

    # Basic stats
    print("Reviews per bank:")
    print(df['bank_name'].value_counts())

    # Plot visualizations
    plot_rating_distribution(df)
    plot_sentiment_distribution(df)

    
    avg_sentiment = df.groupby('bank_name')['sentiment_score'].mean()
    print("\nAverage Sentiment Score per Bank:")
    print(avg_sentiment)

if __name__ == '__main__':
    main()
