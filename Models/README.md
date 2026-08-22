
# 🤖 Models — Crop Recommendation System

This folder contains the serialized machine learning model and encoder artifacts used for inference in the deployed web application.

---

## 📁 Files in This Folder

| File | Size (approx.) | Description |
|------|---------------|-------------|
| `crop_rf_model.pkl` | ~25 MB | Trained Random Forest classifier |
| `label_encoder.pkl` | < 1 KB | LabelEncoder for crop name ↔ integer mapping |
| `README.md` | — | This file |

---

## 🌲 crop_rf_model.pkl

### What It Is
A serialized **Random Forest Classifier** trained on the complete Crop Recommendation Dataset (2,200 records, 22 crop classes, 7 features). This is the final deployment model selected after comparing six ML algorithms under 5-fold stratified cross-validation.

### Model Configuration

| Parameter | Value | Why |
|-----------|-------|-----|
| `n_estimators` | 500 | More trees → more stable predictions |
| `max_depth` | 10 | Prevents overfitting via depth constraint |
| `min_samples_leaf` | 2 | Smooths leaf predictions |
| `min_samples_split` | 5 | Requires meaningful splits |
| `max_features` | log2 | Feature randomization for diversity |
| `criterion` | log_loss | Probabilistic split quality measure |
| `random_state` | 42 | Reproducibility |

> Parameters identified via `RandomizedSearchCV` (n_iter=50, 5-fold CV) in `Notebooks/06_HyperparameterTuning.ipynb`

### Performance

| Metric | Value |
|--------|-------|
| Test Accuracy | **99.55%** |
| CV Accuracy (5-fold mean) | **99.50%** |
| CV Accuracy (5-fold std) | **± 0.30%** |
| Weighted Precision | 99.57% |
| Weighted Recall | 99.55% |
| Weighted F1-Score | 99.55% |
| Training Dataset Size | 1,760 samples (80%) |
| Test Dataset Size | 440 samples (20%) |

### Top Features (by importance)

| Rank | Feature | Importance |
|------|---------|-----------|
| 1 | Humidity | 24.04% |
| 2 | Potassium (K) | 19.83% |
| 3 | Rainfall | 18.72% |
| 4 | Phosphorus (P) | 15.24% |
| 5 | Nitrogen (N) | 15.02% |
| 6 | Temperature | 5.06% |
| 7 | Soil pH | 2.91% |

### Training Details
- **Trained on:** Full dataset (2,200 samples) in `Notebooks/07_SaveModel.ipynb`
- **Serialized with:** `joblib` (Python 3.12, scikit-learn)
- **Input:** 7 numerical features — N, P, K, temperature, humidity, ph, rainfall
- **Output:** Integer class index (0–21), decoded by `label_encoder.pkl`

---

## 🔤 label_encoder.pkl

### What It Is
A serialized **scikit-learn LabelEncoder** fitted on the 22 crop class names. It is used in two directions:

| Direction | Operation | Where Used |
|-----------|-----------|-----------|
| Forward | crop name → integer | Training (encoding target) |
| Inverse | integer → crop name | Deployment (decoding predictions) |

### Encoding Map

| Integer | Crop | Integer | Crop | Integer | Crop |
|---------|------|---------|------|---------|------|
| 0 | apple | 8 | jute | 16 | orange |
| 1 | banana | 9 | kidneybeans | 17 | papaya |
| 2 | blackgram | 10 | lentil | 18 | pigeonpeas |
| 3 | chickpea | 11 | maize | 19 | pomegranate |
| 4 | coconut | 12 | mango | 20 | rice |
| 5 | coffee | 13 | mothbeans | 21 | watermelon |
| 6 | cotton | 14 | mungbean | | |
| 7 | grapes | 15 | muskmelon | | |

### Why It Must Be Saved Separately
The LabelEncoder must be the **exact same object** used during training — it must be loaded alongside the model at inference time to correctly reverse predictions back to human-readable crop names. Re-fitting a new encoder on any other data would produce a different integer mapping and break predictions.

---

## 💻 How to Load and Use These Models

```python
import joblib
import pandas as pd

# Load model and encoder
model = joblib.load('crop_rf_model.pkl')
le    = joblib.load('label_encoder.pkl')

# Prepare input — must match training feature order exactly
sample = pd.DataFrame([[90, 42, 43, 20.87, 82.00, 6.50, 202.93]],
                      columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])

# Predict
encoded_pred = model.predict(sample)
crop_name    = le.inverse_transform(encoded_pred)[0]

print(f"Recommended Crop: {crop_name}")
# Output: Recommended Crop: rice
```

### ⚠️ Important Notes
- **Feature order matters.** Always pass features in this exact order: `N, P, K, temperature, humidity, ph, rainfall`
- **No scaling needed.** The model was trained on raw unscaled features (Random Forest does not require scaling)
- **Python version.** Load in Python 3.12 with the same scikit-learn version used for saving to avoid compatibility issues

---

## 🔄 How These Files Were Generated

```
Notebooks/04_ModelTraining.ipynb      → Baseline training & evaluation
        ↓
Notebooks/05_CrossValidation.ipynb    → 5-fold CV to confirm performance
        ↓
Notebooks/06_HyperparameterTuning.ipynb → Best params via RandomizedSearchCV
        ↓
Notebooks/07_SaveModel.ipynb          → Final model trained on full dataset
                                         → Saves crop_rf_model.pkl
                                         → Saves label_encoder.pkl
```

To regenerate these files, run the notebooks in order from `04` to `07`.

---

## 📦 Serialization Details

| Property | Value |
|----------|-------|
| Library | `joblib` |
| Python Version | 3.12 |
| scikit-learn Version | ≥ 1.4 |
| XGBoost Version | ≥ 2.0 |
| Save Command | `joblib.dump(model, 'crop_rf_model.pkl')` |
| Load Command | `joblib.load('crop_rf_model.pkl')` |

---

## 🌐 Deployment Usage

These model files are used directly by the Flask web application in `WebApp/app.py`:

```python
# From WebApp/app.py
import joblib, os

BASE  = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE, '..', 'Models', 'crop_rf_model.pkl'))
le    = joblib.load(os.path.join(BASE, '..', 'Models', 'label_encoder.pkl'))
```

The web app loads both files at startup and uses them to serve real-time predictions at:  
🔗 **[https://crop-recommendation-system-bfze.onrender.com/](https://crop-recommendation-system-bfze.onrender.com/)**

---

*Part of Module 1 — Crop Recommendation System | AI Smart Farming Assistant*  
*Sharda University, Greater Noida, India*
