# Cyrene Data Collective

Cyrene is an end-to-end analytical solution developed using the **AdventureWorks** dataset. It leverages machine learning to identify high-value customer segments and predicts the probability of customers reaching "Elite" status to drive personalized marketing strategies.

## The Analytical Workflow

### 1. Exploratory Data Analysis (EDA) & Cleaning
We performed an extensive EDA to transform raw transactional data into meaningful insights:
- **Data Cleaning:** Handled inconsistencies in the AdventureWorks relational database and standardized currency/date formats.
- **Behavioral Analysis:** Analyzed purchasing patterns across different demographics and product categories (Bikes, Components, Clothing, Accessories).
- **Outlier Detection:** Identified high-frequency shoppers to distinguish between standard customers and potential "Stars."

### 2. Feature Engineering
To improve model accuracy, we engineered specialized features:
- **Diversity Score:** Capturing the variety of product categories a customer interacts with.
- **Avg_Discount:** Measuring sensitivity to promotions.
- **Weekend Rate:** Analyzing shopping habits based on time-of-week.

### 3. Customer Segmentation (Clustering)
Using **K-Means Clustering**, we grouped customers into 4 distinct "Tribes" based on their purchasing DNA:
- **Pure Performers, Gearheads, Adventurous Mixers, and Style Icons.**

### 4. VIP Probability Model (Random Forest)
The core of Cyrene is a **Random Forest Classifier** that calculates the specific probability of a customer becoming a VIP member.
- **Objective:** Instead of a simple Yes/No, the model outputs a **Probability Score (0 to 1)**.
- **Performance:** Achieved a **0.86 ROC-AUC score**, indicating high predictive power.
- **Feature Importance:** `Avg_Discount` and `Diversity` were identified as the primary drivers of VIP potential.

---

##  VIP Mobile Experience (Conceptual UI)
Since the model identifies the top-tier "Stars" and "High-Probability" customers, we designed a conceptual mobile interface to showcase how this data could be used in a real-world product:
- **Exclusive Recommendations:** Personalized product feeds based on the customer's "Tribe."
- **Limited VIP Offers:** Targeted promotions for customers with high probability scores.

> [!TIP]
> *The mobile application UI serves as a bridge between data science and product design, demonstrating the commercial viability of the model.*

<p align="center">
  <img src="assets/mobile_ui_1.jpeg" width="300">
  <img src="assets/mobile_ui_2.jpeg" width="300">
</p>

---

##  Tech Stack
- **Languages:** Python (Pandas, Scikit-Learn, Plotly)
- **Deployment:** Streamlit (Live Dashboard)
- **Visualization:** Power BI

- **Data Source:** AdventureWorks Dataset
