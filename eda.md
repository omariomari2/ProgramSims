# Exploratory Data Analysis (EDA) Summary Report

## 1. Executive Summary
The initial assessment of the Delinquency Prediction dataset revealed significant structural issues which have been resolved through data recovery. The dataset contains 500 records with 19 attributes. Key findings include missing values in financial fields (`Income`, `Loan_Balance`), inconsistent categorizations in `Employment_Status`, and a correlation between `Credit_Utilization` and `Delinquent_Account`.

## 2. Data Quality Assessment
### 2.1 Structural Integrity
- **Initial State**: The provided XLSX file used a Strict Open XML format that was initially unreadable by standard tools.
- **Resolution**: A custom parsing script was developed to recover 100% of the data, correcting column alignment issues caused by sparse XML storage.

### 2.2 Missing Values
| Column | Missing Count | Percentage | Impact |
| :--- | :--- | :--- | :--- |
| **Income** | 39 | 7.8% | High (Key predictor for risk) |
| **Loan_Balance** | 29 | 5.8% | Medium |
| **Credit_Score** | 2 | 0.4% | Low |

### 2.3 Data Inconsistencies
- **Employment_Status**: Values are inconsistent (e.g., "Employed", "employed", "EMP").
    - *Recommendation*: Standardize to a fixed set: `Employed`, `Unemployed`, `Self-employed`, `Retired`.
- **Zero Values**:
    - `Missed_Payments` (77 zeros): Valid (customer has no missed payments).
    - `Delinquent_Account` (420 zeros): Valid (majority of customers are not delinquent).
    - `Account_Tenure` (28 zeros): Potential new customers.

## 3. Explanatory Data Analysis & Risk Indicators
### 3.1 Correlation Analysis
- **Strongest Predictor**: `Credit_Utilization` shows a strong positive correlation (**0.60**) with `Delinquent_Account`. High utilization is a key risk indicator.
- **Credit Score**: Shows a moderate negative correlation (**-0.55**) with `Delinquent_Account`, validating that lower scores align with higher delinquency.
- **Income**: Moderate negative correlation (**-0.39**). Lower income is associated with higher delinquency.

### 3.2 Categorical Insights
- **Payment History (Months 1-6)**:
    - Recent months (Month_1) show a relatively even split between `On-time` (177), `Missed` (164), and `Late` (159).
    - This high rate of "Missed" and "Late" suggests a high-risk cohort, possibly a targeted collection dataset rather than a general population sample.
- **Location**: Evenly distributed across 5 major cities (Chicago, LA, Phoenix, Houston, NY).

## 4. Recommendations for Modeling
1.  **Imputation**:
    - Impute `Income` and `Loan_Balance` using median values or regression based on `Employment_Status` and `Credit_Score`.
    - Drop rows with missing `Credit_Score` (only 2 records).
2.  **Feature Engineering**:
    - Normalize `Employment_Status`.
    - Encode `Payment_History` (Late/Missed/On-time) into numerical risk scores.
    - Create a `Debt-to-Income` ratio utilizing the recovered `Income` and `Loan_Balance` (check existing `Debt_to_Income_Ratio` consistency).
3.  **Privacy**:
    - `Customer_ID` should be hashed or removed before model training.

## 5. Next Steps
- Approval to proceed with data cleaning (standardization and imputation).
- Initiation of feature selection for the predictive model.