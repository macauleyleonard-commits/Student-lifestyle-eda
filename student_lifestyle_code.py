import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# 1. DATA LOADING & EXPLORATION
def load_and_explore_data(filepath):
    df = pd.read_csv(filepath)
    print("--- Dataset Overview ---")
    print(f"Shape: {df.shape}")
    print("\nFirst 5 Rows:\n", df.head())
    print("\nInfo:")
    df.info()
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nSummary:\n", df.describe())
    return df

# 2. CLEANING - FIXED for new pandas
def clean_data(df):
    df_clean = df.copy()
    before = len(df_clean)
    df_clean.drop_duplicates(inplace=True)
    print(f"\nRemoved {before - len(df_clean)} duplicates.")

    # Fix: don't use inplace=True
    num_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    return df_clean

# 3. ANALYSIS
def compute_correlations(df):
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    print("\n--- Correlation with GPA ---")
    if 'GPA' in corr_matrix.columns:
        print(corr_matrix['GPA'].sort_values(ascending=False))

    # Save to Excel
    with pd.ExcelWriter("student_lifestyle_descriptive_stats.xlsx", engine="openpyxl") as writer:
        df.describe().to_excel(writer, sheet_name="Summary_Stats")
        corr_matrix.to_excel(writer, sheet_name="Correlations")
    print("\nSaved: student_lifestyle_descriptive_stats.xlsx")
    return corr_matrix

# 4. VISUALS - Now focused on GPA
def generate_plots(df, corr_matrix, output_dir="visualizations"):
    os.makedirs(output_dir, exist_ok=True)

    # Distribution + Boxplot for GPA
    plt.figure()
    sns.histplot(df['GPA'], kde=True, color="skyblue")
    plt.title("Distribution of GPA")
    plt.savefig(os.path.join(output_dir, "GPA_distribution.png"))
    plt.close()

    # Key lifestyle vs GPA
    for col in ['Study_Hours', 'Sleep_Hours', 'Social_Media_Hours', 'Physical_Activity']:
        if col in df.columns:
            plt.figure()
            sns.scatterplot(x=df[col], y=df['GPA'], alpha=0.5)
            plt.title(f"{col} vs GPA")
            plt.savefig(os.path.join(output_dir, f"{col}_vs_GPA.png"))
            plt.close()

    # Heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"))
    plt.close()

    print(f"All plots saved in '{output_dir}/'")

# MAIN
if __name__ == "__main__":
    path = "student_lifestyle_dataset.csv"
    if os.path.exists(path):
        data = load_and_explore_data(path)
        cleaned = clean_data(data)
        corr = compute_correlations(cleaned)
        generate_plots(cleaned, corr)
        print("\nPipeline complete!")
    else:
        print(f"File '{path}' not found. Upload CSV first.")
