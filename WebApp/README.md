# 🌐 WebApp — Crop Recommendation System

This folder contains the complete Flask web application that serves the trained Random Forest model as a real-time crop recommendation system, accessible to farmers through any web browser.

---

## 🔗 Live Deployment

🌍 **[https://crop-recommendation-system-bfze.onrender.com/](https://crop-recommendation-system-bfze.onrender.com/)**

Hosted on **Render.com** — free, publicly accessible, no installation required for end users.

---

## 📁 Folder Structure

```
WebApp/
│
├── app.py                  # Flask backend — routes, model loading, prediction logic
│
├── templates/
│   └── index.html          # Frontend — input form + prediction result display
│
├── static/
│   └── style.css           # Styling — layout, colors, responsive design
│
└── README.md               # This file
```

---

## ⚙️ How It Works

```
User opens browser
        ↓
Enters 7 soil & climate values in the form
        ↓
Clicks "Recommend Crop"
        ↓
app.py receives POST request
        ↓
Validates and parses input values
        ↓
Passes values to crop_rf_model.pkl (Random Forest)
        ↓
Model returns encoded integer prediction
        ↓
label_encoder.pkl converts integer → crop name
        ↓
Crop name displayed on the page instantly
```

---

## 📄 File Details

---

### `app.py`

The Flask backend that handles all application logic.

**What it does:**
- Loads `crop_rf_model.pkl` and `label_encoder.pkl` from the `Models/` folder at startup
- Exposes a single route `/` that handles both `GET` (render form) and `POST` (process prediction) requests
- Parses and validates the 7 user inputs from the HTML form
- Passes inputs as a pandas DataFrame to the model in the correct feature order
- Decodes the model's integer output back to a crop name using the label encoder
- Passes the prediction and form data back to `index.html` for display
- Handles input errors gracefully with a user-friendly error message

**Feature input order (must match training):**
```python
FEATURES = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
```

**Key code — prediction logic:**
```python
values   = [float(form_data[f]) for f in FEATURES]
input_df = pd.DataFrame([values], columns=FEATURES)

encoded    = model.predict(input_df)
prediction = le.inverse_transform(encoded)[0].capitalize()
```

---

### `templates/index.html`

The frontend HTML page rendered by Flask using Jinja2 templating.

**What it contains:**
- A clean input form with 7 fields — one for each soil and climate parameter
- Placeholder values and valid input ranges shown as hints below each field
- A submit button that triggers the POST request
- A result section that appears after prediction — shows the recommended crop name
- An error section that appears if invalid input is entered
- Form data is preserved after submission (fields stay filled) using Jinja2 `form_data`

**Input fields:**

| Field | Label | Placeholder | Hint (Range) |
|-------|-------|-------------|--------------|
| N | Nitrogen (N) | e.g. 90 | 0 – 140 |
| P | Phosphorus (P) | e.g. 42 | 5 – 145 |
| K | Potassium (K) | e.g. 43 | 5 – 205 |
| temperature | Temperature (°C) | e.g. 25.5 | 8.8 – 43.7 |
| humidity | Humidity (%) | e.g. 80.5 | 14.3 – 100 |
| ph | Soil pH | e.g. 6.5 | 3.5 – 9.9 |
| rainfall | Rainfall (mm) | e.g. 200 | 20.2 – 298.6 |

---

### `static/style.css`

The CSS stylesheet for the web application.

**What it covers:**
- Full-page green gradient background matching the agriculture theme
- Centered white card layout with rounded corners and shadow
- Dark green gradient header with title and subtitle
- Two-column responsive grid layout for the input fields
- Styled input boxes with green focus border highlight
- Full-width green gradient submit button with hover effect
- Success result card (light green background) showing the recommended crop
- Error result card (light red background) for invalid inputs
- Mobile-friendly layout via CSS Grid

---

## 🚀 Run Locally

### Step 1 — Install dependencies
```bash
pip install flask scikit-learn xgboost joblib pandas numpy
```

### Step 2 — Make sure model files exist
The app loads models from `../Models/` relative to `app.py`. Ensure these files are present:
```
Models/
├── crop_rf_model.pkl
└── label_encoder.pkl
```

If they are missing, run `Notebooks/07_SaveModel.ipynb` first to generate them.

### Step 3 — Run the app
```bash
cd WebApp
python app.py
```

### Step 4 — Open in browser
```
http://127.0.0.1:5000
```

---

## 🧪 Test the App

Use these verified input values to test predictions:

| Test | N | P | K | Temp | Humidity | pH | Rainfall | Expected |
|------|---|---|---|------|----------|----|----------|----------|
| ✅ Rice | 90 | 42 | 43 | 20.87 | 82.00 | 6.50 | 202.93 | Rice |
| ✅ Apple | 21 | 47 | 45 | 21.00 | 92.00 | 6.00 | 112.00 | Apple |
| ✅ Coffee | 104 | 18 | 30 | 23.60 | 60.40 | 6.80 | 140.90 | Coffee |
| ✅ Coconut | 23 | 16 | 30 | 27.00 | 80.00 | 5.80 | 175.00 | Coconut |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend Framework | Flask (Python) |
| ML Inference | scikit-learn Random Forest |
| Model Loading | joblib |
| Data Handling | pandas |
| Frontend | HTML5, CSS3 |
| Templating | Jinja2 (via Flask) |
| Deployment Platform | Render.com |

---

## 🌍 Deployment on Render.com

The app is deployed as a **Web Service** on Render.com.

### Render Configuration

| Setting | Value |
|---------|-------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python app.py` |
| Environment | Python 3 |
| Branch | `main` |
| Auto-Deploy | Enabled (on push to main) |

### requirements.txt (place in root of repo)
```
flask
scikit-learn
xgboost
joblib
pandas
numpy
gunicorn
```

### For production deployment, update `app.py` last line:
```python
# Development
if __name__ == '__main__':
    app.run(debug=True)

# Production (Render uses gunicorn, so debug=False)
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

---

## 📌 Notes

- The app loads both `.pkl` files **once at startup** — not on every request — for fast inference
- Form data is preserved after submission so users don't have to re-enter all values if they want to adjust one field
- Error handling catches both `ValueError` (non-numeric input) and general exceptions, displaying a readable message rather than a 500 error
- The model does **not** require feature scaling at inference time — Random Forest is scale-invariant

---

*Part of Module 1 — Crop Recommendation System | AI Smart Farming Assistant*  
*Sharda University, Greater Noida, India*
