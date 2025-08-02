# FLO Customer Lifetime Value (CLTV) Prediction with BG/NBD and Gamma-Gamma Models

This project focuses on calculating the Customer Lifetime Value (CLTV) for the shoe retailer FLO. [cite_start]The primary goal is to predict the potential value that existing customers will bring to the company in the future, which can help in shaping a long-term roadmap for sales and marketing activities[cite: 3, 8]. [cite_start]The analysis is performed using BG/NBD and Gamma-Gamma models[cite: 2].

[cite_start]The dataset contains information about customers who made purchases through both online and offline channels (OmniChannel) between 2020 and 2021[cite: 12].

---

##  methodological approach

The project is structured into four main tasks: data preparation, creation of the CLTV data structure, model building, and customer segmentation.

### Task 1: Data Preparation

1.  [cite_start]**Data Loading**: The script begins by loading the `flo_data_20k.csv` dataset into a pandas DataFrame[cite: 22].
2.  **Outlier Handling**:
    * [cite_start]Two functions, `outlier_thresholds` and `replace_with_thresholds`, are defined to identify and cap outliers using the 1st and 99th percentiles[cite: 23].
    * [cite_start]This process is applied to the columns: `order_num_total_ever_online`, `order_num_total_ever_offline`, `customer_value_total_ever_offline`, and `customer_value_total_ever_online`[cite: 25, 26].
3.  **Feature Engineering**:
    * [cite_start]To account for omnichannel purchasing behavior, two new features are created[cite: 27]:
        * `order_num_total`: The sum of total online and offline orders.
        * `customer_value_total`: The sum of total online and offline customer value.
4.  [cite_start]**Data Type Conversion**: All columns containing date information are converted to the `datetime` data type for proper time-based calculations[cite: 29].

### Task 2: Creating the CLTV Data Structure

1.  [cite_start]**Set Analysis Date**: The analysis date is set to `2021-06-01`, which is two days after the last recorded purchase in the dataset[cite: 34].
2.  [cite_start]**Create CLTV Metrics**: A new DataFrame named `cltv` is created with the following metrics, which are essential for the probabilistic models[cite: 35]:
    * `recency_cltv_weekly`: The time between a customer's last and first purchase, expressed in weeks.
    * `T_weekly`: The age of the customer (tenure), calculated as the time between the analysis date and their first purchase, in weeks.
    * `frequency`: The number of repeat purchases (total orders - 1).
    * [cite_start]`monetary_cltv_avg`: The average monetary value per purchase[cite: 36].

### Task 3: BG/NBD and Gamma-Gamma Model Implementation

1.  **BG/NBD Model Fitting**:
    * [cite_start]A BetaGeoFitter (BG/NBD) model is fitted on the `frequency`, `recency_cltv_weekly`, and `T_weekly` data to model customer transaction behavior[cite: 40].
    * [cite_start]The model is used to predict the expected number of purchases for each customer over the next 3 and 6 months (`exp_sales_3_month` and `exp_sales_6_month`)[cite: 41, 42].
2.  **Gamma-Gamma Model Fitting**:
    * [cite_start]A GammaGammaFitter model is fitted on the `frequency` and `monetary_cltv_avg` data to model the monetary value of each customer's transactions[cite: 43].
    * [cite_start]The model predicts the expected average profit per transaction for each customer (`exp_average_value`)[cite: 43].
3.  **CLTV Calculation**:
    * [cite_start]The `customer_lifetime_value` function from the `lifetimes` library is used to calculate the 6-month CLTV for each customer by combining the predictions from both the BG/NBD and Gamma-Gamma models[cite: 44].
    * [cite_start]The top 20 customers with the highest CLTV are identified and displayed[cite: 45].

### Task 4: Customer Segmentation

1.  [cite_start]**Segment Creation**: Customers are segmented into four distinct groups (A, B, C, D) based on their 6-month CLTV scores using the `pd.qcut` function[cite: 47]. 'A' represents the most valuable segment.
2.  **Segment Analysis**: The script concludes by performing a detailed analysis of these segments, calculating the mean, min, max, and count of CLTV for each group, as well as the average recency, frequency, and monetary values.

---

## Libraries Used
* `pandas`
* `datetime`
* `lifetimes`
* `sklearn.preprocessing`
* `matplotlib.pyplot`