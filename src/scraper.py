import sys
import os
import time
from datetime import datetime
from tqdm import tqdm
import pandas as pd
from google_play_scraper import app, Sort, reviews
from config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS

class PlayStoreScraper:
    def __init__(self):
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        self.reviews_per_bank = SCRAPING_CONFIG['reviews_per_bank']
        self.lang = SCRAPING_CONFIG['lang']
        self.country = SCRAPING_CONFIG['country']
        self.max_retries = SCRAPING_CONFIG['max_retries']

    def get_app_info(self, app_id):
        try:
            result = app(app_id, lang=self.lang, country=self.country)
            return {
                'app_id': app_id,
                'title': result.get('title', 'N/A'),
                'score': result.get('score', 0),
                'ratings': result.get('ratings', 0),
                'reviews': result.get('reviews', 0),
                'installs': result.get('installs', 'N/A')
            }
        except Exception as e:
            print(f"Error getting app info for {app_id}: {str(e)}")
            return None

    def scrape_reviews(self, app_id, count=400):
        print(f"\nScraping reviews for {app_id}...")
        for attempt in range(self.max_retries):
            try:
                result, _ = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=count
                )
                print(f"Successfully scraped {len(result)} reviews")
                return result
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Failed to scrape reviews after {self.max_retries} attempts")
                    return []

    def process_reviews(self, reviews_data, bank_code):
        processed = []
        for review in reviews_data:
            processed.append({
                'review_id': review.get('reviewId', ''),
                'review_text': review.get('content', ''),
                'rating': review.get('score', 0),
                'review_date': review.get('at', datetime.now()),
                'user_name': review.get('userName', 'Anonymous'),
                'thumbs_up': review.get('thumbsUpCount', 0),
                'reply_content': review.get('replyContent', None),
                'bank_code': bank_code,
                'bank_name': self.bank_names[bank_code],
                'app_version': review.get('reviewCreatedVersion', 'N/A'),
                'source': 'Google Play'
            })
        return processed

    def scrape_all_banks(self):
        all_reviews = []
        print("="*60)
        print("Starting Google Play Store Review Scraper")
        print("="*60)

        for bank_code, app_id in tqdm(self.app_ids.items(), desc="Banks"):
            reviews_data = self.scrape_reviews(app_id, self.reviews_per_bank)
            if reviews_data:
                processed = self.process_reviews(reviews_data, bank_code)
                all_reviews.extend(processed)
            time.sleep(2)

        if all_reviews:
            df = pd.DataFrame(all_reviews)
            os.makedirs(DATA_PATHS['raw'], exist_ok=True)
            df.to_csv(DATA_PATHS['raw_reviews'], index=False)
            print(f"Scraping complete! Saved {len(df)} reviews to {DATA_PATHS['raw_reviews']}")
            return df
        else:
            print("No reviews collected.")
            return pd.DataFrame()

def main():
    scraper = PlayStoreScraper()
    df = scraper.scrape_all_banks()
    return df

if __name__ == "__main__":
    main()
