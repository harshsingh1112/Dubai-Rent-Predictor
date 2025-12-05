import pandas as pd
import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_dubai_rent_data(n=2000):
    """
    Generates a synthetic dataset for Dubai rent prices.
    """
    
    # Locations with approximate 'luxury factor' (Base price multiplier)
    locations = {
        'Downtown Dubai': 1.6,
        'Dubai Marina': 1.4,
        'Palm Jumeirah': 1.8,
        'Jumeirah Beach Residence (JBR)': 1.5,
        'Business Bay': 1.3,
        'Jumeirah Lake Towers (JLT)': 1.1,
        'Jumeirah Village Circle (JVC)': 0.9,
        'Dubai Silicon Oasis': 0.8,
        'Al Nahda': 0.65,
        'International City': 0.55,
        'Discovery Gardens': 0.7,
        'Dubai Sports City': 0.85
    }
    
    data = []
    
    for _ in range(n):
        loc = random.choice(list(locations.keys()))
        loc_factor = locations[loc]
        
        # Bedrooms: Weights favor 1 and 2 beds
        beds = np.random.choice([0, 1, 2, 3, 4], p=[0.15, 0.40, 0.30, 0.10, 0.05])
        
        # Bathrooms usually relate to bedrooms
        if beds == 0:
            baths = 1
        else:
            # Often beds + 1 or equal to beds
            baths = beds + np.random.choice([0, 1])
            
        # Size (sqft) logic
        # Studio: 350-600, 1B: 700-1100, 2B: 1100-1600, 3B: 1600-2500, 4B: 2500-4000
        if beds == 0:
            size_sqft = np.random.randint(350, 650)
        elif beds == 1:
            size_sqft = np.random.randint(700, 1200)
        elif beds == 2:
            size_sqft = np.random.randint(1100, 1700)
        elif beds == 3:
            size_sqft = np.random.randint(1700, 2600)
        else:
            size_sqft = np.random.randint(2500, 4500)
            
        # Furnishing
        furnishing = np.random.choice(['Unfurnished', 'Partly Furnished', 'Furnished'], p=[0.5, 0.1, 0.4])
        furnish_factor = 1.0
        if furnishing == 'Furnished':
            furnish_factor = 1.25
        elif furnishing == 'Partly Furnished':
            furnish_factor = 1.1
            
        # Base Rent Calculation logic
        # Base annual rent per sqft roughly 60-100 AED
        # We add a small premium for higher bedroom counts (efficiency/utility per sqft)
        # But usually smaller units have higher per-sqft price. 
        # However, to ensure total price sensitivity to bedroom count for fixed size:
        base_rate = np.random.uniform(60, 90)
        
        # Apply factors
        # Add a fixed premium per bedroom to distinguish layouts of same size
        # e.g. 1000sqft 1B vs 1000sqft 2B -> 2B pays higher
        bed_premium = beds * 5000 
        
        predicted_rent = (size_sqft * base_rate * loc_factor * furnish_factor) + bed_premium
        
        # Add random noise/variability (market variance) +/- 10%
        noise = np.random.uniform(0.9, 1.1)
        final_rent = int(predicted_rent * noise)
        
        # Round to nearest 1000 for realistic looking prices
        final_rent = round(final_rent / 1000) * 1000
        
        data.append({
            'location': loc,
            'bedrooms': beds,
            'bathrooms': baths,
            'size_sqft': size_sqft,
            'furnishing': furnishing,
            'rent_price': final_rent
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating synthetic Dubai rent data...")
    df = generate_dubai_rent_data(2000)
    
    # Save to CSV
    output_file = 'rent_data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Data generated successfully! Saved to {output_file}")
    print(df.head())
    print("\nPrice stats by Location:")
    print(df.groupby('location')['rent_price'].mean().sort_values(ascending=False))
