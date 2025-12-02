# B8W2: Customer Experience Analytics for Fintech Apps

## Project Overview
This repository contains the customer experience analysis for three major Ethiopian mobile banking apps. The objective is to help **Omega Consultancy** identify satisfaction drivers, pain points, user themes, and opportunities for app improvement.

### Banks Analyzed
- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

### Project Objectives
- Collect and scrape user reviews from the Google Play Store  
- Clean and preprocess raw data  
- Perform sentiment analysis (positive, neutral, negative)  
- Extract themes and high-frequency keywords  
- Provide data-driven insights and recommendations  

---

## Task Summary

### **Task 1 — Data Collection & Preprocessing**
- Scraped **1,200 reviews** (400 per bank)  
- Removed duplicates and empty reviews  
- Removed unsupported Amharic content (**48 reviews**)  
- Normalized dates → `YYYY-MM-DD`  
- Clean preprocessed dataset included in repository  

---

### **Task 2 — Sentiment & Thematic Analysis**

#### Sentiment Analysis (VADER – NLTK)
Each review is classified as:
- **Positive**
- **Neutral**
- **Negative**

#### Theme Extraction
Main themes identified:
- **Account Access Issues**
- **Transaction Performance**
- **User Interface & Experience**
- **Customer Support**
- **Feature Requests**

Additional analysis:
- TF-IDF used to extract top keywords per bank.

---

## Key Insights

### **Satisfaction Drivers**
- Clean and intuitive UI  
- Reliable transactions  
- Good overall usability  

### **Pain Points**
- Slow transfers and app freezes  
- Login / OTP failures  
- Missing key features such as biometric login & notifications  

---

## Sentiment Summary per Bank

| Bank | Positive | Neutral | Negative |
|------|----------|---------|----------|
| **CBE** | 59.95% | 32.46% | 7.59% |
| **BOA** | 48.57% | 31.43% | 20.00% |
| **Dashen** | 66.49% | 21.04% | 12.47% |

---

## Recommendations
- Improve **transaction speed** and overall stability  
- Resolve login and OTP reliability issues  
- Enhance UI/UX for smoother navigation  
- Add highly requested features:
  - Biometric login  
  - Push notifications  
  - Budgeting tools  
- Integrate an **AI-powered chatbot** for faster support  


