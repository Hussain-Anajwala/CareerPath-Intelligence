# Dataset Card — Student Career Assessment Dataset

## Dataset Summary
- **Dataset Name**: Student Career Assessment Dataset
- **Primary Location**: `data/raw/student_career_data.csv`
- **File SHA-256**: `cd9b2d1ce8d1d582f1e472a7dcb2724f687e22ac5932d5760eac95c53d281d62`
- **Row Count**: 6,901
- **Column Count**: 20
- **Feature Count**: 19 input columns (98 preprocessed features)
- **Target Column**: `Suggested Job Role` (12 classes)
- **Class Imbalance Ratio**: 1.17 (mild imbalance)

## License & Attribution
- **License**: `UNVERIFIED — primary-source license evidence pending`
- **Attribution**: Kaggle Educational Open Data repo (source verification pending)

## Data Splitting & Leakage Controls
- **Train Split**: 5,520 rows (80%)
- **Holdout Test Split**: 1,381 rows (20%)
- **Random Seed**: 42 (Stratified by target)
- **Leakage Controls**: All preprocessors (Imputer, Standard Scaler, OneHotEncoder) fit strictly on train split ONLY.
