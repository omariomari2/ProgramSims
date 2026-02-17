
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data(filepath):
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_data(df):
    if df is None:
        return

    print("Shape:", df.shape)
    print("\nInfo:")
    print(df.info())
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nDuplicates:")
    print(df.duplicated().sum())
    print("\nIdentify 0 values where they might be missing data:")
    numerical_cols = df.select_dtypes(include=['number']).columns
    for col in numerical_cols:
        zeros = (df[col] == 0).sum()
        if zeros > 0:
            print(f"{col}: {zeros} zeros")

    print("\nSummary Statistics:")
    print(df.describe())

    print("\nCorrelation Matrix:")
    corr = df[numerical_cols].corr()
    print(corr)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.savefig('correlation_matrix.png')
    plt.close()

    for col in numerical_cols:
        plt.figure()
        sns.histplot(df[col], kde=True)
        plt.title(f'Distribution of {col}')
        plt.savefig(f'dist_{col}.png')
        plt.close()

    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        print(f"\nValue Counts for {col}:")
        print(df[col].value_counts())
        plt.figure()
        sns.countplot(y=df[col])
        plt.title(f'Count of {col}')
        plt.savefig(f'count_{col}.png')
        plt.close()

if __name__ == "__main__":
    filepath = "recovered_data.csv"
    if os.path.exists(filepath):
        import sys
        with open("eda_report.log", "w") as f:
            sys.stdout = f
            df = load_data(filepath)
            analyze_data(df)
            sys.stdout = sys.__stdout__
            print("Report generated: eda_report.log")
    else:
        print(f"File not found: {filepath}")
