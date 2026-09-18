"""Audit script for raw dataset student_career_data.csv."""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
import pandas as pd
from careerpath.data.loaders import DataLoader
from careerpath.data.validators import DataValidator

file_path = Path('data/raw/student_career_data.csv')
df, sha256 = DataLoader.load_tabular_data(file_path)

print("=== DATASET OVERVIEW ===")
print(f"File Path: {file_path}")
print(f"SHA-256: {sha256}")
print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")

print("\n=== TARGET AUDIT: Suggested Job Role ===")
target_audit = DataValidator.audit_target(df, "Suggested Job Role")
for k, v in target_audit.items():
    print(f"  {k}: {v}")

print("\n=== TARGET CLASS DISTRIBUTION ===")
vc = df["Suggested Job Role"].value_counts()
for role, count in vc.items():
    pct = (count / len(df)) * 100
    print(f"  - '{role}': {count} samples ({pct:.2f}%)")

print("\n=== LEAKAGE AUDIT ===")
leakage_res = DataValidator.audit_leakage(df, target_column="Suggested Job Role")
print(f"Is leakage detected: {leakage_res.is_leakage_detected}")
print(f"Suspicious columns: {leakage_res.suspicious_columns}")
print(f"Findings: {leakage_res.findings}")

print("\n=== COLUMN AUDIT & CARDINALITY ===")
for col in df.columns:
    col_type = df[col].dtype
    nunique = df[col].nunique()
    missing = df[col].isnull().sum()
    sample_vals = df[col].unique()[:5].tolist()
    print(f"Column: '{col}' | Type: {col_type} | Unique: {nunique} | Missing: {missing}")
    print(f"  Sample values: {sample_vals}")

print("\n=== CATEGORICAL FREQUENCY TABLES ===")
for col in df.select_dtypes(include=['object']).columns:
    print(f"\n--- Column: '{col}' ({df[col].nunique()} unique) ---")
    print(df[col].value_counts().to_dict())
