import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

def train():
    print("Loading dataset (this may take a moment)...")
    # Fetch Ames Housing dataset (ID 42165 corresponds to standard Ames Housing, or use name='house_prices')
    try:
        housing = fetch_openml(name="house_prices", as_frame=True)
    except Exception as e:
        print(f"Error fetching dataset: {e}")
        return

    df = housing.frame
    
    # Feature Selection
    features = ['OverallQual', 'GrLivArea', 'GarageCars', 'FullBath', 'YearBuilt', 'TotalBsmtSF']
    target = 'SalePrice'
    
    print(f"Selected features: {features}")
    
    # Some older versions of the dataset might have minimal nan differences, handling explicitly
    X = df[features].copy()
    y = df[target]
    
    # Impute missing values
    print("Handling missing values...")
    X = X.fillna(X.median())
    
    # Scaling
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Train
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.4f}")
    
    # Save
    print("Saving model and scaler...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'house_price_model.pkl')
    scaler_path = os.path.join(script_dir, 'scaler.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Saved model to {model_path}")
    print(f"Saved scaler to {scaler_path}")
    
    # Verify
    print("Verifying reload...")
    loaded_model = joblib.load(model_path)
    if loaded_model:
        print("Model reload successful.")

if __name__ == "__main__":
    train()
