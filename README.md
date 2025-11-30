# B8W2: Customer Experience Analytics for Fintech Apps

## Project Overview

This repository contains the analysis of user reviews for **three Ethiopian bank mobile apps** to help Omega Consultancy understand customer satisfaction, pain points, and feature requests.

**Banks Analyzed:**
- Commercial Bank of Ethiopia (CBE)  
- Bank of Abyssinia (BOA)  
- Dashen Bank  

**Objectives:**
1. Scrape user reviews from Google Play Store.  
2. Preprocess and clean review data.  
3. Perform sentiment analysis to classify reviews as positive, neutral, or negative.  
4. Extract themes and keywords to identify satisfaction drivers and pain points.  
5. Prepare actionable insights for app improvement.  


---

## Repository Structure

bank-reviews-analytics/
│
├── data/
│   ├── raw/                 # Raw scraped reviews (original Google Play data)
│   └── processed/           # Cleaned, deduplicated, preprocessed datasets
│
├── src/
│   ├── scraper.py           # Scrapes Google Play Store reviews
│   ├── preprocessing.py     # Cleans, normalizes, and deduplicates review text
│   ├── sentiment_analysis.py# Performs sentiment scoring & keyword extraction
│   └── config.py            # Configuration: paths, constants, settings
│
├── notebooks/
│   └── Task2_Sentiment_Analysis.ipynb   # Notebook for exploration & visualization
│
├── requirements.txt         # Project dependencies
└── README.md                # Documentation, description, and setup guide



---

## Task Summary

### Task 1 – Data Collection & Preprocessing
- Scraped **1,200 reviews** (400 per bank).  
- Removed **duplicates** & **missing reviews**.  
- Filtered out **Amharic text** (48 reviews removed).  
- Normalized dates (`YYYY-MM-DD`).  
- Cleaned dataset saved at:  


### Task 2 – Sentiment & Thematic Analysis
- Sentiment analysis using **VADER (NLTK)**:  
  - Labels: `positive`, `neutral`, `negative`.  
- Theme extraction:
  - `Account Access Issues`  
  - `Transaction Performance`  
  - `User Interface & Experience`  
  - `Customer Support`  
  - `Feature Requests`  
- Top **TF-IDF keywords** extracted per bank.  
- Results saved at:  

## Key Insights

### Satisfaction Drivers
- Clean & intuitive **UI/UX**.  
- Reliable **transactions** and app performance.  

### Pain Points
- **Slow transfers** and app crashes.  
- **Login/OTP failures**.  
- Limited requested features: biometric login, notifications, budgeting tools.  

**Bank Sentiment Summary:**

| Bank   | Positive | Neutral | Negative |
|--------|----------|--------|----------|
| CBE    | 59.95%   | 32.46% | 7.59%    |
| BOA    | 48.57%   | 31.43% | 20.00%   |
| Dashen | 66.49%   | 21.04% | 12.47%   |

---

## Recommendations

1. Optimize **transaction speed** and overall app performance.  
2. Fix **account access issues** (login, OTP).  
3. Improve **UI/UX** further for ease of navigation.  
4. Add requested features: **biometric login, notifications, budgeting tools**.  
5. Implement **AI chatbot** for faster complaint resolution.  




