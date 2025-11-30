import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from config import DATA_PATHS
import nltk
import os


nltk.download('vader_lexicon')


THEMES = {
    'Account Access Issues': ['login', 'password', 'sign in', 'forgot', 'blocked', 'otp'],
    'Transaction Performance': ['slow', 'transfer', 'crash', 'timeout', 'lag', 'loading'],
    'User Interface & Experience': ['ui', 'navigation', 'easy', 'clunky', 'design', 'interface'],
    'Customer Support': ['support', 'help', 'agent', 'response', 'service'],
    'Feature Requests': ['fingerprint', 'budget', 'notification', 'feature', 'update', 'biometric']
}

def assign_themes(review):
    """
    Returns a list of themes that match the review text.
    """
    matched_themes = []
    text_lower = str(review).lower()

    for theme, keywords in THEMES.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                matched_themes.append(theme)
                break

    if not matched_themes:
        matched_themes.append('Other')

    return matched_themes



class SentimentAnalyzer:
    def __init__(self, input_csv=DATA_PATHS['processed_reviews']):
        self.input_csv = input_csv
        self.df = None
        self.sia = SentimentIntensityAnalyzer()

    
    def load_data(self):
        self.df = pd.read_csv(self.input_csv)

        
        self.df["review"] = self.df["review"].astype(str).str.strip()

        
        if "bank" not in self.df.columns and "bank_code" in self.df.columns:
            self.df.rename(columns={"bank_code": "bank"}, inplace=True)

        print(f"Loaded {len(self.df)} reviews")


    def analyze_sentiment(self):
        """
        Adds sentiment_score and sentiment_label columns.
        """
        def get_label(score):
            if score >= 0.05:
                return "positive"
            elif score <= -0.05:
                return "negative"
            else:
                return "neutral"

        self.df["sentiment_score"] = self.df["review"].apply(
            lambda x: self.sia.polarity_scores(str(x))["compound"]
        )
        self.df["sentiment_label"] = self.df["sentiment_score"].apply(get_label)

        print("Sentiment analysis completed.")

    
    def extract_keywords(self, top_n=10):
        """
        Extract top TF-IDF keywords per bank.
        """
        keywords_per_bank = {}

        for bank_name in self.df["bank"].unique():
            bank_reviews = (
                self.df[self.df["bank"] == bank_name]["review"]
                .astype(str)
                .tolist()
            )

            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2),
                max_features=top_n
            )

            try:
                vectorizer.fit(bank_reviews)
                keywords_per_bank[bank_name] = vectorizer.get_feature_names_out().tolist()
            except ValueError:
                
                keywords_per_bank[bank_name] = []

        return keywords_per_bank

    
    def assign_themes_to_reviews(self):
        """
        Adds theme labels for each review.
        """
        self.df["themes"] = self.df["review"].apply(
            lambda text: ", ".join(assign_themes(text))
        )
        print("Theme assignment completed.")

   
    def print_sentiment_summary(self):
        """
        Prints sentiment distribution per bank (recommended for reporting).
        """
        print("\nSentiment Summary by Bank:")
        print(self.df.groupby("bank")["sentiment_label"].value_counts(normalize=True))

    
    def save_results(self, output_csv=DATA_PATHS["sentiment_results"]):
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        self.df.to_csv(output_csv, index=False)
        print(f"Saved results to {output_csv}")


def main():
    analyzer = SentimentAnalyzer()
    analyzer.load_data()

    analyzer.analyze_sentiment()

    keywords = analyzer.extract_keywords()
    print("\nTop keywords per bank:")
    for bank, kw in keywords.items():
        print(f"{bank}: {kw}")

    analyzer.assign_themes_to_reviews()
    analyzer.print_sentiment_summary()

    analyzer.save_results()


if __name__ == "__main__":
    main()
