from http.server import BaseHTTPRequestHandler
import json
import joblib
import pandas as pd
import numpy as np
import os

# Load model at startup
# Note: Vercel functions have the file in the same directory
try:
    model_path = os.path.join(os.path.dirname(__file__), 'rent_model.pkl')
    model = joblib.load(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Load data for market insights
try:
    csv_path = os.path.join(os.path.dirname(__file__), 'rent_data.csv')
    df = pd.read_csv(csv_path)
    print("Data loaded successfully")
except Exception as e:
    print(f"Error loading data: {e}")
    df = None

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            if model is None:
                raise ValueError("Model not initialized")

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Prepare input dataframe
            location = data.get('location')
            input_df = pd.DataFrame([{
                'location': location,
                'bedrooms': int(data.get('bedrooms')),
                'bathrooms': float(data.get('bathrooms')),
                'size_sqft': float(data.get('size_sqft')),
                'furnishing': data.get('furnishing')
            }])
            
            # Predict
            prediction = model.predict(input_df)[0]
            predicted_rounded = round(prediction / 1000) * 1000
            
            # Market Insights (Histogram Data)
            market_buckets = []
            if df is not None and location in df['location'].values:
                # Filter by location and roughly similar bedroom count (optional, but location is main)
                loc_df = df[df['location'] == location]
                
                # Create histogram buckets (numpy)
                counts, bin_edges = np.histogram(loc_df['rent_price'], bins=10)
                
                for i in range(len(counts)):
                    market_buckets.append({
                        'range_start': int(bin_edges[i]),
                        'range_end': int(bin_edges[i+1]),
                        'count': int(counts[i]),
                        'label': f"{int(bin_edges[i]/1000)}k"
                    })
            
            response = {
                'status': 'success',
                'predicted_price': predicted_rounded,
                'currency': 'AED',
                'market_data': market_buckets
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            error_response = {
                'status': 'error',
                'message': str(e)
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
