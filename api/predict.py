from http.server import BaseHTTPRequestHandler
import json
import joblib
import numpy as np
import os
import csv

# Load model at startup
try:
    model_path = os.path.join(os.path.dirname(__file__), 'rent_model.pkl')
    model = joblib.load(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Load data for market insights (Lightweight CSV reading)
market_data_cache = []
try:
    csv_path = os.path.join(os.path.dirname(__file__), 'rent_data.csv')
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Store only needed columns: location and rent_price
            market_data_cache.append({
                'location': row['location'],
                'rent_price': float(row['rent_price'])
            })
    print(f"Data loaded successfully: {len(market_data_cache)} rows")
except Exception as e:
    print(f"Error loading data: {e}")

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
            
            location = data.get('location')
            
            # Prepare input array (List of lists or 2D numpy array)
            # Order: location, bedrooms, bathrooms, size_sqft, furnishing
            input_features = [[
                location,
                int(data.get('bedrooms')),
                float(data.get('bathrooms')),
                float(data.get('size_sqft')),
                data.get('furnishing')
            ]]
            
            # Predict
            prediction = model.predict(input_features)[0]
            predicted_rounded = round(prediction / 1000) * 1000
            
            # Market Insights (Histogram Data) using Numpy
            market_buckets = []
            
            # Filter prices for location
            # This list comp is fast enough for <10k rows
            loc_prices = [
                d['rent_price'] for d in market_data_cache 
                if d['location'] == location
            ]
            
            if loc_prices:
                # Create histogram buckets (numpy)
                counts, bin_edges = np.histogram(loc_prices, bins=10)
                
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
