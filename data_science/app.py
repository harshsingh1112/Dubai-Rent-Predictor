import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Dubai Rent Predictor", 
    page_icon="🏙️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    /* Main Background & Text */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(45deg, #2E86C1, #1ABC9C);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26, 188, 156, 0.4);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 188, 156, 0.6);
        background: linear-gradient(45deg, #1ABC9C, #2E86C1);
    }
    
    /* Cards/Containers */
    .metric-card {
        background-color: #21262D;
        border: 1px solid #30363D;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Highlight Text */
    .highlight-text {
        font-size: 1.2rem;
        font-weight: 500;
        color: #8B949E;
    }
    
    /* Custom Dividers */
    hr {
        border-color: #30363D;
    }
    </style>
    """, unsafe_allow_html=True)

# Load model and data
@st.cache_resource
def load_model():
    model = joblib.load('rent_model.pkl')
    return model

@st.cache_data
def load_data():
    df = pd.read_csv('rent_data.csv')
    return df

try:
    model = load_model()
    df = load_data()
except FileNotFoundError:
    st.error("Model or Data file not found. Please run 'generate_data.py' and 'model_training.py' first.")
    st.stop()

# Header Section
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🏙️ Dubai Rent Predictor")
    st.markdown("<p style='font-size: 1.2rem; color: #8B949E;'>AI-powered fair rent estimation & deal evaluation engine.</p>", unsafe_allow_html=True)
with col_head2:
    st.image("https://img.icons8.com/color/96/000000/dubai.png", width=80) 

st.divider()

# Sidebar Inputs with better visuals
st.sidebar.markdown("### 🏠 Property Config")

locations = sorted(df['location'].unique())
location = st.sidebar.selectbox("📍 Location", locations)

col_side1, col_side2 = st.sidebar.columns(2)
with col_side1:
    bedrooms = st.sidebar.selectbox("🛌 Beds", [0, 1, 2, 3, 4], format_func=lambda x: "Studio" if x == 0 else f"{x}")
with col_side2:
    default_baths = 1 if bedrooms == 0 else bedrooms + 1
    bathrooms = st.sidebar.number_input("🚿 Baths", 1, 6, default_baths)

size_sqft = st.sidebar.slider("📐 Size (sq. ft)", 300, 5000, 800, 50)
furnishing = st.sidebar.selectbox("🛋️ Furnishing", ['Unfurnished', 'Partly Furnished', 'Furnished'])

# Create input dataframe
input_data = pd.DataFrame({
    'location': [location],
    'bedrooms': [bedrooms],
    'bathrooms': [bathrooms],
    'size_sqft': [size_sqft],
    'furnishing': [furnishing]
})

# Prediction Logic
predicted_price = model.predict(input_data)[0]
predicted_rounded = round(predicted_price / 1000) * 1000

# Main Dashboard Layout
col_main1, col_main2 = st.columns([1, 1.2])

with col_main1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("💰 Predicted Fair Rent")
    st.markdown(f"<h1 style='color: #1ABC9C; font-size: 3.5rem;'>AED {predicted_rounded:,.0f}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='highlight-text'>Per Year</p>", unsafe_allow_html=True)
    st.markdown(f"Properties in similar condition in **{location}** typically trade around this range.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("") # Spacer
    
    # Deal Evaluator
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("⚖️ Deal Evaluator")
    listing_price = st.number_input("Enter Actual Listing Price (AED)", value=int(predicted_rounded), step=1000)
    
    if listing_price > 0:
        diff = listing_price - predicted_price
        pct_diff = (diff / predicted_price) * 100
        
        if pct_diff > 15:
            st.error(f"⚠️ Overpriced by {pct_diff:.1f}%")
            st.caption("Negotiate harder! This is significantly above market rate.")
        elif pct_diff < -10:
            st.success(f"🔥 Good Deal! Underpriced by {abs(pct_diff):.1f}%")
            st.caption("Grab this deal before it's gone.")
        else:
            st.info(f"✅ Fair Price (Within {pct_diff:.1f}%)")
            st.caption("This lists at a reasonable market rate.")
            
    st.markdown('</div>', unsafe_allow_html=True)

with col_main2:
    # Plotly Visualization
    st.subheader(f"📊 Market Insights: {location}")
    
    loc_data = df[df['location'] == location]
    
    # Histogram
    fig = px.histogram(
        loc_data, 
        x="rent_price", 
        nbins=20, 
        title=f"Rent Distribution in {location}",
        color_discrete_sequence=['#2E86C1'],
        opacity=0.8
    )
    
    # Add vertical lines
    fig.add_vline(x=predicted_price, line_width=3, line_dash="dash", line_color="#1ABC9C", annotation_text="Suggested", annotation_position="top left")
    if listing_price > 0:
        fig.add_vline(x=listing_price, line_width=3, line_dash="dot", line_color="#E74C3C", annotation_text="Listed", annotation_position="top right")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        xaxis_title="Annual Rent (AED)",
        yaxis_title="Count",
        bargap=0.1
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plot: Size vs Price
    fig2 = px.scatter(
        loc_data, 
        x="size_sqft", 
        y="rent_price", 
        color="bedrooms", 
        title="Size vs. Rent Price (by Bedroom Count)",
        color_continuous_scale="Viridis"
    )
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA')
    )
    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.divider()
st.caption("Developed with ❤️ by Your Name | Data is synthetic for demonstration purposes.")
