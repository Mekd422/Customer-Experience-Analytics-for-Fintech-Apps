import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from dotenv import load_dotenv

load_dotenv()

# --------------------------
# Step 1: Load data from DB
# --------------------------
def get_reviews_df():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    query = """
    SELECT b.bank_name, r.review_text, r.rating, r.sentiment_label, r.sentiment_score, r.review_date
    FROM reviews r
    JOIN banks b ON r.bank_id = b.bank_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --------------------------
# Step 2: Basic visualizations
# --------------------------
def plot_rating_distribution(df):
    plt.figure(figsize=(8,6))
    sns.countplot(data=df, x='rating', hue='bank_name')
    plt.title('Rating Distribution by Bank')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.legend(title='Bank')
    plt.tight_layout()
    plt.savefig('outputs/figures/rating_distribution.png')
    plt.show()

def plot_sentiment_distribution(df):
    plt.figure(figsize=(8,6))
    sns.countplot(data=df, x='sentiment_label', hue='bank_name', order=['positive', 'neutral', 'negative'])
    plt.title('Sentiment Distribution by Bank')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.legend(title='Bank')
    plt.tight_layout()
    plt.savefig('outputs/figures/sentiment_distribution.png')
    plt.show()

# --------------------------
# Step 3: Word clouds per bank
# --------------------------
def generate_wordclouds(df):
    for bank in df['bank_name'].unique():
        text = " ".join(df[df['bank_name'] == bank]['review_text'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='tab10').generate(text)
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud for {bank}')
        plt.tight_layout()
        plt.savefig(f'outputs/figures/wordcloud_{bank.replace(" ", "_")}.png')
        plt.show()

# --------------------------
# Step 4: Top pain points / themes
# --------------------------
def top_keywords(df, top_n=10):
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    for bank in df['bank_name'].unique():
        reviews = df[df['bank_name'] == bank]['review_text'].dropna()
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
        X = vectorizer.fit_transform(reviews)
        scores = dict(zip(vectorizer.get_feature_names_out(), X.sum(axis=0).tolist()[0]))
        top_terms = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        print(f"\nTop {top_n} keywords/themes for {bank}:")
        for term, score in top_terms:
            print(f"{term} ({score:.2f})")

# --------------------------
# Step 5: Sentiment trends over time
# --------------------------
def plot_sentiment_trends(df):
    df['review_date'] = pd.to_datetime(df['review_date'])
    trend = df.groupby(['bank_name', pd.Grouper(key='review_date', freq='W')])['sentiment_score'].mean().reset_index()
    
    plt.figure(figsize=(10,6))
    sns.lineplot(data=trend, x='review_date', y='sentiment_score', hue='bank_name', marker='o')
    plt.title('Weekly Sentiment Trend per Bank')
    plt.xlabel('Week')
    plt.ylabel('Average Sentiment Score')
    plt.legend(title='Bank')
    plt.tight_layout()
    plt.savefig('outputs/figures/sentiment_trend.png')
    plt.show()

# --------------------------
# Step 6: Main
# --------------------------
def main():
    df = get_reviews_df()

    # Basic stats
    print("Reviews per bank:")
    print(df['bank_name'].value_counts())

    # Plot visualizations
    plot_rating_distribution(df)
    plot_sentiment_distribution(df)

    # Word clouds
    generate_wordclouds(df)

    # Top themes / keywords
    top_keywords(df, top_n=10)

    # Sentiment trends over time
    plot_sentiment_trends(df)

    # Average sentiment
    avg_sentiment = df.groupby('bank_name')['sentiment_score'].mean()
    print("\nAverage Sentiment Score per Bank:")
    print(avg_sentiment)

if __name__ == '__main__':
    main()
