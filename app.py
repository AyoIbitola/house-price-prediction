from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load Model and Scaler
MODEL_PATH = os.path.join('model', 'house_price_model.pkl')
SCALER_PATH = os.path.join('model', 'scaler.pkl')

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Model and Scaler loaded successfully.")
except Exception as e:
    print(f"Error loading model/scaler: {e}")
    model = None
    scaler = None

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_text = ""
    
    if request.method == 'POST':
        if not model or not scaler:
            return render_template('index.html', prediction_text="Error: Model not loaded.")
        
        try:
            # Get values (Order: OverallQual, GrLivArea, GarageCars, FullBath, YearBuilt, TotalBsmtSF)
            features = [
                float(request.form['OverallQual']),
                float(request.form['GrLivArea']),
                float(request.form['GarageCars']),
                float(request.form['FullBath']),
                float(request.form['YearBuilt']),
                float(request.form['TotalBsmtSF'])
            ]
            
            # Preprocess
            features_array = np.array([features])
            features_scaled = scaler.transform(features_array)
            
            # Predict
            prediction = model.predict(features_scaled)[0]
            
            prediction_text = f"Estimated House Price: ${prediction:,.2f}"
            
        except ValueError:
            prediction_text = "Error: Please enter valid numerical values."
        except Exception as e:
            prediction_text = f"Error: {str(e)}"

    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)
