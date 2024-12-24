import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import base64
import os

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Set page config
st.set_page_config(page_title="Restaurant Recommender", layout="wide")

# Load data
df = pd.read_csv(os.path.join(DATA_DIR, 'preprocessed', 'recommendation_data.csv'))

# Function to load and encode the background image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%%;
        height: 100%%;
        background-color: rgba(14, 17, 23, 0.5);
        z-index: -1;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background image
set_png_as_page_bg(os.path.join(ASSETS_DIR, 'bg.jpg'))

# Custom CSS
st.markdown("""
<style>
    /* Font preloading */
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');

    /* Apply the font globally */
    * {
        font-family: 'Source Sans Pro', sans-serif;
    }

    /* Sidebar styling */   
    .css-1d391kg {
        background-color: rgba(26, 28, 35, 0.8);
    }
    
    /* Grid container for cards */
    div.row-widget.stHorizontalBlock {
        gap: 20px;
        padding: 10px;
        display: flex;
        justify-content: space-between;
    }
    
    /* Restaurant cards */
    div[data-testid="column"] {
        background-color: rgba(26, 28, 35, 0.6);
        padding: 20px;
        border-radius: 10px;
        margin: 0 !important;
        border: 1px solid #2d2d2d;
        height: 250px;
        display: flex;
        flex-direction: column;
        backdrop-filter: blur(10px);
        flex: 0 1 calc(33.333% - 14px);
        margin-bottom: 20px !important;
    }

    /* For last row when not full */
    div[data-testid="column"]:last-child:nth-child(3n - 1) {
        margin-right: calc(33.333% + 14px) !important;
    }
    
    div[data-testid="column"]:last-child:nth-child(3n - 2) {
        margin-right: calc(66.666% + 28px) !important;
    }

    /* Restaurant card content wrapper */
    .restaurant-card {
        background-color: rgba(26, 28, 35, 0.6);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2d2d2d;
        height: 100%;
        display: flex;
        flex-direction: column;
        backdrop-filter: blur(10px);
    }

    /* Restaurant name styling */
    .restaurant-name {
        color: #9370DB;
        font-size: 1.5em;
        margin-bottom: 15px;
    }

    /* Restaurant details styling */
    .restaurant-details {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    /* Headers */
    h1 {
        color: #9370DB;
        font-family: 'Helvetica Neue', sans-serif;
        padding: 20px 0px;
    }
    
    h2 {
        color: #B19CD9;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #9370DB;
        color: white;
        border-radius: 5px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #B19CD9;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the dataset"""
    df = pd.read_csv(os.path.join(DATA_DIR, 'preprocessed', 'recommendation_data.csv'))
    return df

# Load data
df = load_data()

# Define columns
categorical_cols = ['Cuisine', 'Restaurant_City', 'Price', 'Alcohol_Service', 'Parking']
numerical_cols = ['Overall_Rating', 'Food_Rating', 'Service_Rating']

# Preprocessing
encoder = OneHotEncoder(sparse_output=False)
encoded_categorical = encoder.fit_transform(df[categorical_cols])

scaler = MinMaxScaler()
normalized_numerical = scaler.fit_transform(df[numerical_cols])

# Combine features
features = pd.DataFrame(
    data=np.hstack([encoded_categorical, normalized_numerical]),
    columns=encoder.get_feature_names_out(categorical_cols).tolist() + numerical_cols
)

def recommend_restaurants(input_features, df, features, n_recommendations=3):
    """
    Recommends restaurants based on user preferences.
    
    Args:
        input_features (dict): User's preferences
        df (pd.DataFrame): Original dataset
        features (pd.DataFrame): Preprocessed feature matrix
        n_recommendations (int): Number of recommendations to return
    
    Returns:
        pd.DataFrame: Top N recommended restaurants
    """
    # Convert input features into the same format as feature matrix
    input_data = pd.DataFrame([input_features])
    encoded_input = encoder.transform(input_data[categorical_cols])
    normalized_input = scaler.transform(input_data[numerical_cols])
    
    # Combine encoded and normalized input features
    input_vector = np.hstack([encoded_input, normalized_input])
    
    # Calculate similarity scores
    similarity_scores = cosine_similarity(input_vector, features.values)[0]
    
    # Add similarity scores to the original dataframe
    df['Similarity'] = similarity_scores
    
    # Sort by similarity scores and get top N recommendations
    df_sorted = df.sort_values(by='Similarity', ascending=False)
    
    # Remove duplicates based on restaurant name
    recommendations = []
    seen_restaurants = set()
    
    for _, row in df_sorted.iterrows():
        if row['Restaurant_Name'] not in seen_restaurants:
            recommendations.append(row)
            seen_restaurants.add(row['Restaurant_Name'])
            
        if len(recommendations) == n_recommendations:
            break
    
    # Convert recommendations to DataFrame
    recommendations_df = pd.DataFrame(recommendations)[['Restaurant_Name', 'Cuisine', 'Restaurant_City', 'Price', 'Alcohol_Service', 'Parking', 'Overall_Rating']]
    recommendations_df.index = range(1, len(recommendations_df) + 1)
    
    return recommendations_df

# Add a header with custom styling
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🍽️ Restaurant Recommendation System</h1>
    </div>
""", unsafe_allow_html=True)

# Create the input form
st.sidebar.header("Enter Your Preferences")

# Get unique values for categorical fields
cuisines = sorted(df['Cuisine'].unique())
cities = sorted(df['Restaurant_City'].unique())
price_levels = sorted(df['Price'].unique())
alcohol_options = sorted(df['Alcohol_Service'].unique())
parking_options = sorted(df['Parking'].unique())

# Create input widgets
selected_cuisine = st.sidebar.selectbox("Select Cuisine", cuisines)
selected_city = st.sidebar.selectbox("Select City", cities)
selected_price = st.sidebar.selectbox("Select Price Range", price_levels)
selected_alcohol = st.sidebar.selectbox("Alcohol Service", alcohol_options)
selected_parking = st.sidebar.selectbox("Parking Available", parking_options)

# Rating inputs
st.sidebar.header("Rate Importance (1-3)")
overall_rating = st.sidebar.slider("Overall Rating", 1, 3, 2)
food_rating = st.sidebar.slider("Food Rating", 1, 3, 2)
service_rating = st.sidebar.slider("Service Rating", 1, 3, 2)

# Number of recommendations
n_recommendations = st.sidebar.slider("Number of Recommendations", 1, 10, 5)

if st.sidebar.button("Get Recommendations"):
    input_features = {
        'Cuisine': selected_cuisine,
        'Restaurant_City': selected_city,
        'Price': selected_price,
        'Alcohol_Service': selected_alcohol,
        'Parking': selected_parking,
        'Overall_Rating': overall_rating,
        'Food_Rating': food_rating,
        'Service_Rating': service_rating
    }
    
    recommendations = recommend_restaurants(input_features, df, features, n_recommendations)
    
    st.markdown("<h2>Recommended Restaurants</h2>", unsafe_allow_html=True)
    
    num_rows = (len(recommendations) + 2) // 3
    
    for row in range(num_rows):
        cols = st.columns(3)
        for col_idx in range(3):
            idx = row * 3 + col_idx + 1
            
            if idx <= len(recommendations):
                with cols[col_idx]:
                    row_data = recommendations.loc[idx]
                    st.markdown(f"""
                        <div class="restaurant-card">
                            <div class="restaurant-name">
                                {idx}. {row_data['Restaurant_Name']}
                            </div>
                            <div class="restaurant-details">
                                <p>🍴 <b>Cuisine:</b> {row_data['Cuisine']}</p>
                                <p>📍 <b>Location:</b> {row_data['Restaurant_City']}</p>
                                <p>💰 <b>Price:</b> {row_data['Price']}</p>
                                <p>🍷 <b>Alcohol:</b> {row_data['Alcohol_Service']}</p>
                                <p>🅿️ <b>Parking:</b> {row_data['Parking']}</p>
                                <p>⭐ <b>Rating:</b> {row_data['Overall_Rating']:.1f}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div class='stInfo' style='text-align: center;'>
            <h4>
                👈 Please fill in your preferences and click 'Get Recommendations' to get started!
            </h4>
        </div>
    """, unsafe_allow_html=True)