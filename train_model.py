import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

# 1. Data Ingestion
file_path = 'c:/Users/owusu/Documents/lod/recovered_data.csv'
print(f"Loading data from {file_path}...")
df = pd.read_csv(file_path)

# 2. Preprocessing & Cleaning
# Standardize Employment_Status
df['Employment_Status'] = df['Employment_Status'].astype(str).str.lower().str.strip()
employment_map = {
    'employed': 'Employed', 'emp': 'Employed', 
    'self-employed': 'Self-employed', 'self': 'Self-employed',
    'unemployed': 'Unemployed', 'unemp': 'Unemployed',
    'retired': 'Retired'
}
df['Employment_Status'] = df['Employment_Status'].map(employment_map).fillna('Other')

# Impute Missing Values
# Income & Loan_Balance: Fill with median
imputer = SimpleImputer(strategy='median')
df[['Income', 'Loan_Balance']] = imputer.fit_transform(df[['Income', 'Loan_Balance']])

# Drop rows with missing target or crucial identifiers if any (though EDA said mostly clean)
df.dropna(subset=['Delinquent_Account'], inplace=True)

# 3. Feature Engineering
# Debt-to-Income Ratio
df['DTI_Ratio'] = df['Loan_Balance'] / (df['Income'] + 1) # +1 to avoid div by zero

# Payment History Risk Score
# Weighted sum of misses/lates if columns exist. 
payment_cols = [c for c in df.columns if 'Month_' in c]
def calculate_risk_score(row):
    score = 0
    for col in payment_cols:
        status = str(row[col]).lower()
        if 'missed' in status:
            score += 2
        elif 'late' in status:
            score += 1
    return score

if payment_cols:
    df['Payment_Risk_Score'] = df.apply(calculate_risk_score, axis=1)

# Encode Categoricals
le = LabelEncoder()
df['Employment_Status_Code'] = le.fit_transform(df['Employment_Status'])

# Select Features for Model
features = ['Credit_Utilization', 'Credit_Score', 'Income', 'Loan_Balance', 'DTI_Ratio', 'Employment_Status_Code']
if payment_cols:
    features.append('Payment_Risk_Score')

target = 'Delinquent_Account'

X = df[features]
y = df[target]

# 4. Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 5. Model Training (XGBoost)
print("\nTraining XGBoost Model...")
# Use basic params
model = xgb.XGBClassifier(
    objective='binary:logistic',
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    eval_metric='logloss',
    use_label_encoder=False
)
model.fit(X_train, y_train)

# 6. Evaluation
y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred = model.predict(X_test)

auc = roc_auc_score(y_test, y_pred_proba)
print(f"\nModel Performance:")
print(f"AUC-ROC: {auc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature Importance
print("\nFeature Importance:")
importance = model.feature_importances_
feat_imp = pd.DataFrame({'Feature': features, 'Importance': importance}).sort_values(by='Importance', ascending=False)
print(feat_imp.to_string(index=False))
