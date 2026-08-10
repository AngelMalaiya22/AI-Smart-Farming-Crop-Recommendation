# Dataset

This folder contains the datasets used for the **Crop Recommendation** module of the AI Smart Farming Assistant project.

The datasets are maintained in different stages to keep the data preparation and machine learning workflow organized.

## 📂 Dataset Files

### 1. `original_dataset.csv`

The original dataset collected from Kaggle. It contains the raw agricultural features and crop-related information before any modifications or feature engineering.

### 2. `enhanced_dataset.xlsx`

The enhanced version of the original dataset.

Changes made during dataset engineering include:
- Removal of unnecessary features
- Addition of the `Soil_Type` feature
- Manual rule-based assignment of soil types using agricultural context such as **Season, Region, Crop Type, and Soil Texture**

This is the finalized dataset used as the basis for the Crop Recommendation model.

### 3. `encoded_dataset.csv`

The processed version of the enhanced dataset prepared for machine learning.

It contains:
- Selected relevant features
- One-Hot Encoded categorical features
- Label Encoded `Crop_Type` target
- Features removed during feature selection

This dataset is used as the input for the **model training stage**.

## 🔄 Dataset Workflow

```text
original_dataset.csv
        ↓
Data Cleaning & Feature Engineering
        ↓
enhanced_dataset.xlsx
        ↓
Feature Selection & Encoding
        ↓
encoded_dataset.csv
        ↓
Model Training
