import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

def train_model():
    print("Loading data...")
    import os
    # Assuming script is in data_science/ and csv is adjacent
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'rent_data.csv')
    df = pd.read_csv(csv_path)
    
    # Features and Target
    X = df[['location', 'bedrooms', 'bathrooms', 'size_sqft', 'furnishing']]
    y = df['rent_price']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing Pipeline
    # OneHotEncode 'location' (index 0) and 'furnishing' (index 4)
    # Passthrough numericals: 'bedrooms' (1), 'bathrooms' (2), 'size_sqft' (3)
    
    # We use indices because we want to pass numpy arrays in production to avoid Pandas dependency
    categorical_features = [0, 4]
    numerical_features = [1, 2, 3]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', 'passthrough', numerical_features)
        ]
    )
    
    # Model Pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    print("Training Random Forest model (Numpy mode)...")
    # Convert to numpy array (values) to strip column names
    model.fit(X_train.values, y_train)
    
    # Evaluation
    print("Evaluating model...")
    y_pred = model.predict(X_test.values)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"Mean Absolute Error: AED {mae:.2f}")
    print(f"Root Mean Squared Error: AED {rmse:.2f}")
    
    # Baseline comparison (Mean Baseline)
    baseline_pred = np.full(len(y_test), y_train.mean())
    baseline_mae = mean_absolute_error(y_test, baseline_pred)
    print(f"Baseline (Mean) MAE: AED {baseline_mae:.2f}")
    
    if mae < baseline_mae:
        print("Model is performing better than baseline.")
    
    # Save model
    print("Saving model artifacts...")
    joblib.dump(model, 'rent_model.pkl')
    # We dump the whole pipeline so preprocessing is included!
    
    print("Done.")

if __name__ == "__main__":
    train_model()
