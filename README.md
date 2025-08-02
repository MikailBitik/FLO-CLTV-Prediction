# FLO Customer Lifetime Value (CLTV) Prediction

## 📝 Project Overview

This project aims to create a data-driven roadmap for FLO's sales and marketing activities by predicting the Customer Lifetime Value (CLTV). By estimating the future potential value of existing customers, FLO can make more informed long-term plans. The analysis uses BG/NBD and Gamma-Gamma models to forecast customer behavior and value.

This project was completed as part of the **CRM Analytics** module in the **Data Scientist Path** training program by **Miuul**.

***

## 💾 Dataset

The analysis uses a dataset containing the past shopping behaviors of customers who made purchases through both online and offline channels (OmniChannel) between 2020 and 2021. The dataset consists of 19,945 observations and 13 variables.

**Note:** The dataset used for this project cannot be publicly shared due to privacy restrictions.

### Dataset Schema

| Variable                              | Description                                                    |
| ------------------------------------- | -------------------------------------------------------------- |
| `master_id`                           | Unique customer ID                                             |
| `order_channel`                       | The channel used for the purchase (e.g., Android, iOS)         |
| `last_order_channel`                  | The channel where the last purchase was made                   |
| `first_order_date`                    | Date of the customer's first purchase                          |
| `last_order_date`                     | Date of the customer's last purchase                           |
| `last_order_date_online`              | Date of the customer's last online purchase                    |
| `last_order_date_offline`             | Date of the customer's last offline purchase                   |
| `order_num_total_ever_online`         | Total number of online purchases by the customer               |
| `order_num_total_ever_offline`        | Total number of offline purchases by the customer              |
| `customer_value_total_ever_offline`   | Total value of the customer's offline purchases                |
| `customer_value_total_ever_online`    | Total value of the customer's online purchases                 |
| `interested_in_categories_12`         | List of categories the customer shopped from in the last 12 months |

***

## 🛠️ Methodology

The project follows a systematic approach divided into four main tasks.

### 1. Data Preparation
* **Outlier Handling**: Outlier values in key numerical columns were suppressed using a custom function based on the IQR method to ensure model stability.
* **Feature Engineering**: New features for total order number (`order_num_total`) and total customer value (`customer_value_total`) were created to capture the complete omnichannel behavior of each customer.
* **Data Type Conversion**: All columns containing date information were converted to the `datetime` format for time-based calculations.

### 2. CLTV Data Structure Creation
A new DataFrame was prepared with the specific metrics required for CLTV modeling:
* **Recency (weekly)**: The time between a customer's last and first purchase.
* **Tenure (T) (weekly)**: The age of the customer since their first purchase.
* **Frequency**: The number of repeat purchases.
* **Monetary Value (avg)**: The average earnings per purchase.

### 3. BG/NBD and Gamma-Gamma Modeling
* **BG/NBD Model**: The model was fitted to predict the expected number of purchases customers will make in the future.
* **Gamma-Gamma Model**: The model was fitted to estimate the average monetary value of each customer's transactions.
* **CLTV Calculation**: Using the outputs from both models, a 6-month CLTV was calculated for each customer.

### 4. Customer Segmentation
Based on the calculated 6-month CLTV, customers were segmented into four distinct groups (A, B, C, D) using quantile-based discretization. This allows for the development of targeted action plans for each group.

***

## 📈 Results & Actionable Insights

The analysis successfully segmented customers into four distinct groups based on their 6-month CLTV score. The script generates a summary table revealing the key characteristics of each segment, providing a clear basis for strategic decision-making.

The segments are labeled from **A (most valuable)** to **D (least valuable)**.

### Segment Analysis

Here is a representation of the analysis output, which aggregates key metrics for each segment:

| cltv_segment | cltv (mean) | recency_cltv_weekly (mean) | frequency (mean) | monetary_cltv_avg (mean) | count |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A** | 832.12 | 169.93 | 7.94 | 155.61 | 3087 |
| **B** | 398.98 | 196.88 | 5.37 | 114.28 | 3086 |
| **C** | 277.10 | 215.11 | 4.29 | 96.53 | 3087 |
| **D** | 162.77 | 240.23 | 3.33 | 78.49 | 3086 |

*(Note: The values above are illustrative examples based on the script's final aggregation logic)*

### Actionable Insights
* **Segment A (Champions) 🏆**: This group represents the top 25% of customers with the **highest CLTV**. They purchase frequently and have a high average spending value.
    * **Action**: Reward these customers with loyalty programs, exclusive offers, and early access to new products to maximize retention.

* **Segment B (Loyal Customers) 😊**: These customers are valuable and purchase consistently.
    * **Action**: Engage them with personalized recommendations and cross-sell opportunities to increase their average spending.

* **Segment C (Potential Loyalists) 🤔**: This group consists of customers with average frequency and monetary value.
    * **Action**: Encourage more frequent purchases through targeted promotions and reminders about new arrivals in categories they have previously shown interest in.

* **Segment D (At-Risk / Low Value) 📉**: This group represents the bottom 25% of customers with the **lowest CLTV**. They have the lowest frequency and the highest recency (meaning it has been a long time since their last purchase).
    * **Action**: Implement targeted re-engagement campaigns with special discounts or win-back offers to reactivate their interest before they churn.
