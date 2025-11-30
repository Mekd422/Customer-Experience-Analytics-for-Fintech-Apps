import pandas as pd
from config import DATA_PATHS
import re


AMHARIC_PATTERN = re.compile(r'[\u1200-\u137F]')

def contains_amharic(text):
    if not isinstance(text, str):
        return False
    return bool(AMHARIC_PATTERN.search(text))


def preprocess_reviews():
    df = pd.read_csv(DATA_PATHS['raw_reviews'])

    
    df = df.rename(columns={'review_text': 'review', 'review_date': 'date'})

    
    df.dropna(subset=['review'], inplace=True)

   
    original_len = len(df)
    df = df[~df['review'].apply(contains_amharic)]
    removed_count = original_len - len(df)
    print(f"Removed {removed_count} Amharic reviews")

    
    df.drop_duplicates(subset=['review', 'rating', 'date'], inplace=True)

    
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

    
    df.dropna(subset=['date'], inplace=True)

    
    df.to_csv(DATA_PATHS['processed_reviews'], index=False)
    print(f"Preprocessing complete! Cleaned data saved to {DATA_PATHS['processed_reviews']}")


if __name__ == "__main__":
    preprocess_reviews()
