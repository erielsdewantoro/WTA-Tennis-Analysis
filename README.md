# WTA Tennis Match Analysis & Odds Predictability Dashboard

![WTA Dashboard Preview](wta-dashboard.png)

### ► [View the Interactive Dashboard](https://erieldewantoro-wta-tennis-analysis.streamlit.app/)

---

## Project Overview

This project is an end-to-end data analysis of over **42,000** Women's Tennis Association (WTA) matches from 2006 to 2025. The primary objective is to uncover patterns and trends in match distribution and player performance, while also conducting an in-depth analysis of bookmaker prediction accuracy based on provided odds.

The findings are visualized in an interactive Power BI dashboard, which consists of two main pages: **Matches Overview** and **Odds Predictability Analysis**.

---

## Dataset

The dataset used in this project was sourced from **Kaggle**. It includes detailed information for each match, such as:
- Tournament details (name, date, surface type).
- Player information (winner and loser).
- Match statistics (number of sets).
- Betting odds data from various bookmakers.

---

## Methodology & Technology

1.  **Data Wrangling & EDA (Exploratory Data Analysis):** The initial data cleaning, transformation, and exploratory analysis were performed using **Python** with the **Pandas** and **NumPy** libraries.
2.  **Data Visualization & Dashboarding:** The processed data was then loaded into **Power BI** to create the data model and build interactive visualizations.

---

## Dashboard Deep Dive

The dashboard is divided into two main analytical sections:

### 1. Page: WTA Matches Overview (2006–2025)
This page provides a high-level overview of the WTA tournament landscape.

**Main KPIs:**
- **Total Matches:** 42,815
- **Unique Players:** 2,148
- **Average Sets per Match:** 2.33
- **Upset Rate:** 34.8%

**Key Visualizations:**
- **Annual Match & Upset Rate Trend:** Shows the fluctuation in the total number of matches and the upset rate year over year.
- **Top 10 Players by Total Wins:** Identifies the most dominant players in the dataset, led by Wozniacki (588 wins).
- **Match Distribution by Round:** Reveals that nearly half (47.3%) of all matches occur in the first round.
- **Match Distribution by Surface:** Highlights the dominance of **Hard Courts** (26K matches) compared to Clay (12K) and Grass (5K).

### 2. Page: Predictability of Matches by Odds
This page focuses on analyzing how accurately bookmaker odds predict match outcomes.

**Main KPIs:**
- **Overall Odds Accuracy:** 49.70% (nearly a coin toss).
- **Average Odds Gap:** 50%
- **Total Upsets:** 34.8% of matches were won by the underdog.

**Key Visualizations:**
- **Annual Odds Accuracy Trend:** Shows how bookmaker accuracy has fluctuated over time, generally staying between 40-55%.
- **Odds Accuracy by Surface:** Provides insight that predictions are most accurate on **Greenset (59%)** and least accurate on **Carpet (47%)**.
- **Odds Gap vs. Correct Prediction Relationship:** Confirms the hypothesis that the larger the odds gap between players, the higher the probability of a correct prediction by the bookmaker.
- **Accuracy Matrix by Round and Surface:** Offers a granular analysis showing how accuracy varies depending on the combination of tournament round and surface type.

---

## Key Findings & Insights

- **Bookmaker Predictions Are Not Always Reliable:** With an accuracy of only **49.70%**, odds should not be considered the sole predictor of a match's outcome.
- **Upsets are Common:** Over a third (34.8%) of matches ended with the underdog winning, indicating a high level of competition on the WTA Tour.
- **Surface Specialization is a Key Factor:** The dominance of matches on Hard Courts highlights the importance of performance on this surface. Furthermore, the varying odds accuracy across different surfaces suggests unique performance variables on each.
- **Dominant Players:** A small group of players, including Wozniacki, Azarenka, and Serena Williams, consistently won a large number of matches during this period.
