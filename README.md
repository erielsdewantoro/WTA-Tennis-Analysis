# WTA Tennis Match Analysis

![WTA Dashboard Preview](Dashboard.png)

### ► [View the Interactive Dashboard](https://erieldewantoro-wta-tennis-analysis.streamlit.app/)

---

## Project Overview

This project is an end-to-end data analysis of over **42,000** Women's Tennis Association (WTA) matches from 2006 to 2025. The primary objective is to uncover patterns and trends in match distribution, player performance, and upset rates.

The findings are summarized in the Power BI dashboard snapshot above and are fully explorable in the interactive Streamlit application linked.

---

## Methodology & Technology

1.  **Data Wrangling & EDA:** The initial data cleaning, transformation, and exploratory analysis were performed using **Python (Pandas, NumPy)**.
2.  **Data Visualization & Dashboarding:** An initial static dashboard was built in **Power BI** to establish key metrics.
3.  **Web App Deployment:** The analysis was migrated to an interactive web application using **Streamlit** and **Plotly** for dynamic filtering and visualization, then deployed to the cloud.

---

## Dashboard Deep Dive & Key Insights

This single-page dashboard summarizes the key findings from over 42,000 matches, focusing on distribution, top players, and upset trends.

### Main KPIs (2006-2025)
* **Total Matches:** 42,810+
* **Unique Players:** 812
* **Average Sets per Match:** 3.33
* **Upset Rate:** 29.57%

### Key Highlights & Visualizations
* **High Upset Rate:** As noted in the highlights, nearly **30%** of all matches end in an upset, indicating a high level of competition on the tour.
* **Hard Court Dominance:** The 'Pertandingan PerLapang' (Matches by Surface) treemap clearly shows that **'Hard'** court is the most dominant surface, hosting over **50%** of all matches.
* **Consistent Elite Players:** Despite the high upset rate, the 'Top 10 Pemain' chart shows that a core group of elite players (led by Wozniacki, Azarenka, and S. Williams) consistently dominated in total wins over this period.
* **Annual Upset Trend:** The line chart reveals the fluctuation of upset rates year over year, allowing for analysis of the tour's predictability over time.
