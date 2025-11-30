import pandas as pd
from config import DATA_PATHS

def preprocess_reviews():
    df = pd.read_csv(DATA_PATHS['raw_reviews'])

    # Rename columns
    df = df.rename(columns={'review_text': 'review', 'review_date': 'date'})

    # Remove duplicates and missing values
    df.drop_duplicates(subset=['review', 'rating', 'date'], inplace=True)
    df.dropna(subset=['review'], inplace=True)

    # Normalize dates
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # Save processed CSV
    df.to_csv(DATA_PATHS['processed_reviews'], index=False)
    print(f"Preprocessing complete! Cleaned data saved to {DATA_PATHS['processed_reviews']}")

if __name__ == "__main__":
    preprocess_reviews()
