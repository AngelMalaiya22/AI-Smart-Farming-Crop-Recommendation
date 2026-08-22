from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)

BASE  = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE, '..', 'Models', 'crop_rf_model.pkl'))
le    = joblib.load(os.path.join(BASE, '..', 'Models', 'label_encoder.pkl'))

FEATURES = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error      = None
    form_data  = {}

    if request.method == 'POST':
        try:
            form_data = {f: request.form[f] for f in FEATURES}
            values    = [float(form_data[f]) for f in FEATURES]
            input_df  = pd.DataFrame([values], columns=FEATURES)

            encoded     = model.predict(input_df)
            prediction  = le.inverse_transform(encoded)[0].capitalize()

        except ValueError:
            error = "Please enter valid numbers in all fields."
        except Exception as e:
            error = f"Something went wrong: {str(e)}"

    return render_template('index.html',
                           prediction=prediction,
                           error=error,
                           form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
