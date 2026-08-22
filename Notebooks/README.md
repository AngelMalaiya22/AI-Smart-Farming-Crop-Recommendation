
# 📓 Notebooks — Crop Recommendation System

This folder contains all Jupyter Notebooks developed for Module 1 of the AI Smart Farming Assistant project. The notebooks are numbered sequentially and must be run in order to reproduce the complete ML pipeline — from raw data to a saved, deployment-ready model.

---

## 📁 Notebooks Overview

| # | Notebook | Purpose | Key Output |
|---|----------|---------|------------|
| 01 | `01_DataPreprocessing.ipynb` | Load, inspect, and clean the dataset | Clean dataset ready for analysis |
| 02 | `02_EDA.ipynb` | Explore distributions, correlations, patterns | Visualizations and statistical insights |
| 03 | `03_Encoding.ipynb` | Encode the target variable | `encoded_dataset.csv` |
| 04 | `04_ModelTraining.ipynb` | Train and evaluate all 6 ML models | Model performance comparison table |
| 05 | `05_CrossValidation.ipynb` | 5-fold stratified cross-validation | Mean ± std accuracy for all models |
| 06 | `06_HyperparameterTuning.ipynb` | Tune Random Forest via RandomizedSearchCV | Best hyperparameter configuration |
| 07 | `07_SaveModel.ipynb` | Train final model and serialize artifacts | `crop_rf_model.pkl`, `label_encoder.pkl` |

---

## 🔁 Execution Order

> **Always run notebooks in sequence — each depends on the previous.**

```
01_DataPreprocessing
        ↓
02_EDA
        ↓
03_Encoding  ──────────────────→  Dataset/encoded_dataset.csv
        ↓
04_ModelTraining
        ↓
05_CrossValidation
        ↓
06_HyperparameterTuning
        ↓
07_SaveModel  ─────────────────→  Models/crop_rf_model.pkl
                                   Models/label_encoder.pkl
```

---

## 📋 Notebook Details

---

### 📘 01_DataPreprocessing.ipynb
**Purpose:** Load the raw dataset and perform all quality checks before any analysis or modelling.

**What's covered:**
- Loading `Crop_recommendation.csv` using pandas
- Inspecting dataset shape, column names, and data types
- Checking for missing values across all features
- Checking for duplicate records
- Verifying value ranges for each numerical feature
- Confirming class distribution of the target variable (22 crops × 100 samples each)
- Saving the clean dataset for downstream notebooks

**Key finding:** Dataset contains zero missing values, zero duplicates, and is perfectly balanced — no cleaning required beyond verification.

**Libraries used:** `pandas`, `numpy`

---

### 📗 02_EDA.ipynb
**Purpose:** Perform exploratory data analysis to understand feature distributions, relationships, and class separability before building models.

**What's covered:**
- Distribution plots (histplot + KDE) for all 7 numerical features
- Box plots for outlier detection per feature per crop
- Correlation heatmap (Pearson) among all features
- Crop class distribution bar chart
- Per-feature bar charts showing mean values across crop classes (N, P, K, temperature, humidity, pH, rainfall vs crop type)
- Crosstab analysis of categorical relationships

**Key findings:**
- Humidity and rainfall show multi-modal distributions — strong separability signal
- P and K are moderately correlated (0.74)
- All features show meaningful variation across crop classes

**Libraries used:** `pandas`, `numpy`, `matplotlib`, `seaborn`

---

### 📙 03_Encoding.ipynb
**Purpose:** Convert the categorical target variable (`label`) into numerical integers required by scikit-learn classifiers.

**What's covered:**
- Applying `LabelEncoder` from scikit-learn to the `label` column
- Verifying the encoding map (22 crop names → integers 0–21, alphabetical order)
- Confirming no information is lost in the encoded version
- Saving the encoded dataset as `Dataset/encoded_dataset.csv`

**Important note:** The 7 input features (N, P, K, temperature, humidity, ph, rainfall) are already numerical — only the target column required encoding.

**Libraries used:** `pandas`, `sklearn.preprocessing.LabelEncoder`

---

### 📕 04_ModelTraining.ipynb
**Purpose:** Train all six machine learning classifiers on the dataset and evaluate their performance on a held-out test set.

**What's covered:**
- Stratified train-test split (80% train / 20% test, `random_state=42`)
- Feature scaling using `StandardScaler` (fitted on train only — no leakage)
- Training and evaluation of 6 classifiers:
  - Random Forest (`criterion='log_loss'`)
  - Decision Tree (`criterion='entropy'`)
  - XGBoost (`reg_lambda=1`)
  - SVM (`gamma=1`)
  - Logistic Regression (`C=100, max_iter=1000`)
  - KNN (`metric='minkowski', p=3`)
- Classification report (precision, recall, F1-score) for each model
- Confusion matrix for each model
- Feature importance plot (Random Forest)
- Train vs test accuracy comparison (to check for overfitting)

**Results:**

| Model | Test Accuracy |
|-------|--------------|
| Random Forest | **99.55%** |
| Decision Tree | 99.09% |
| SVM | 99.09% |
| XGBoost | 99.09% |
| Logistic Regression | 98.41% |
| KNN | 98.18% |

**Libraries used:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `sklearn`, `xgboost`

---

### 📒 05_CrossValidation.ipynb
**Purpose:** Apply 5-fold stratified cross-validation to all six models to obtain statistically robust performance estimates beyond a single train-test split.

**What's covered:**
- `StratifiedKFold` (n_splits=5, shuffle=True, random_state=42)
- `Pipeline` wrapping `StandardScaler` + each classifier to prevent fold-level data leakage
- `cross_validate` with scoring: accuracy, F1 weighted, precision weighted, recall weighted
- Mean and standard deviation reported across 5 folds for each model
- Bar chart with error bars comparing all models

**Results:**

| Model | CV Accuracy (Mean ± Std) |
|-------|--------------------------|
| Random Forest | **99.50% ± 0.30%** |
| XGBoost | 99.36% ± 0.39% |
| SVM | 98.73% ± 0.37% |
| Decision Tree | 98.50% ± 0.37% |
| Logistic Regression | 98.09% ± 0.37% |
| KNN | 97.09% ± 0.62% |

**Key insight:** Cross-validation reveals XGBoost ranks 2nd (not 4th as in the single split), demonstrating that CV provides a more reliable model ranking than a single evaluation.

**Libraries used:** `pandas`, `numpy`, `matplotlib`, `sklearn`

---

### 📔 06_HyperparameterTuning.ipynb
**Purpose:** Systematically optimize the Random Forest hyperparameters using `RandomizedSearchCV` to find the best model configuration.

**What's covered:**
- Defining the hyperparameter search space
- Running `RandomizedSearchCV` (n_iter=50, cv=5, scoring='accuracy', n_jobs=-1)
- Printing best parameters and best CV score
- Evaluating the tuned model on the test set
- Comparing baseline vs tuned accuracy

**Search space:**

| Parameter | Values Searched |
|-----------|----------------|
| `n_estimators` | 100, 200, 300, 500 |
| `max_depth` | 10, 15, 20, None |
| `min_samples_leaf` | 1, 2, 4 |
| `min_samples_split` | 2, 5, 10 |
| `max_features` | sqrt, log2 |
| `criterion` | gini, entropy, log_loss |

**Best parameters found:**
```
n_estimators=500, max_depth=10, min_samples_leaf=2,
min_samples_split=5, max_features=log2, criterion=log_loss
Best CV Accuracy: 99.55%
```

**Libraries used:** `pandas`, `numpy`, `sklearn`

---

### 📃 07_SaveModel.ipynb
**Purpose:** Train the final Random Forest model using the best hyperparameters on the complete dataset (all 2,200 samples) and serialize it for deployment.

**What's covered:**
- Loading the full dataset (not just train split)
- Training Random Forest with tuned hyperparameters on all 2,200 samples
- Verifying train accuracy on full data
- Saving `crop_rf_model.pkl` using `joblib`
- Saving `label_encoder.pkl` using `joblib`
- Loading the saved files and running a test prediction to verify correctness

**Verification test:**
```
Input:  N=90, P=42, K=43, Temp=20.87, Humidity=82, pH=6.5, Rainfall=202.93
Output: rice ✅
```

**Why train on the full dataset?**
For deployment, we want the model to have seen as much data as possible. Since hyperparameters were already validated via cross-validation and tuning, training on 100% of the data (rather than 80%) gives the deployed model the best possible generalization.

**Libraries used:** `pandas`, `numpy`, `sklearn`, `joblib`

---

## ⚙️ Environment Setup

### Install dependencies
```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost joblib jupyter
```

### Or with conda
```bash
conda install numpy pandas matplotlib seaborn scikit-learn jupyter
pip install xgboost joblib
```

### Launch Jupyter
```bash
jupyter notebook
```

### Tested with
| Package | Version |
|---------|---------|
| Python | 3.12 |
| scikit-learn | ≥ 1.4 |
| XGBoost | ≥ 2.0 |
| pandas | ≥ 2.0 |
| numpy | ≥ 1.26 |
| matplotlib | ≥ 3.8 |
| seaborn | ≥ 0.13 |
| joblib | ≥ 1.3 |

---

## 📌 Notes

- All notebooks use `random_state=42` for reproducibility
- `StandardScaler` is always fitted **only on training data** — never on test or validation data
- Cross-validation uses `Pipeline` to ensure the scaler is re-fitted per fold, preventing data leakage
- Notebook 07 trains on the **complete** 2,200-sample dataset (not the 80% split) for maximum deployment performance

---

*Part of Module 1 — Crop Recommendation System | AI Smart Farming Assistant*  
*Sharda University, Greater Noida, India*
