# Restaurant Recommendation System

A **Streamlit-based web application** that delivers personalized restaurant recommendations tailored to user preferences. This project leverages data-driven insights to enhance user experience.

## 📁 Project Structure

```
Restaurant_Recommendation_System/
├── assets/
│   └── bg.jpg
├── data/
│   ├── cleaned/
│   │   ├── cleaned_consumers.csv
│   │   └── cleaned_restaurant.csv
│   ├── preprocessed/
│   │   └── recommendation_data.csv
│   └── raw/
│       ├── Data Dictionary/
│       │   └── data_dictionary.csv
│       ├── consumer_preferences.csv
│       ├── consumers.csv
│       ├── ratings.csv
│       ├── restaurant_cuisines.csv
│       └── restaurants.csv  
├── notebooks/
│   ├── Data_cleaning_consumers.ipynb
│   ├── Data_cleaning_restaurant.ipynb
│   └── recommendation.ipynb
├── src/
│   └── app.py
└── requirements.txt
```

## 🔧 Project Components

### **Data Pipeline**
1. **Raw Data** (`/data/raw/`)
   - Contains original datasets and data dictionaries.
2. **Data Cleaning** (`/notebooks/`)
   - `Data_cleaning_consumers.ipynb`: Preprocess consumer data.
   - `Data_cleaning_restaurant.ipynb`: Preprocess restaurant data.
   - `recommendation.ipynb`: Build the recommendation system.
3. **Cleaned Data** (`/data/cleaned/`)
   - Stores processed consumer and restaurant datasets.
4. **Preprocessed Data** (`/data/preprocessed/`)
   - `recommendation_data.csv`: Consolidated dataset for recommendations.

### **Web Application**
- **Frontend** (`/src/app.py`)
  - Streamlit interface for personalized recommendations.

## 🧣️ Data Cleaning & Preprocessing

### Data Cleaning Process (`/notebooks/Data_cleaning_consumers.ipynb`, `Data_cleaning_restaurant.ipynb`)

1. **Restaurant Data Cleaning**
   - Handling missing values in all columns
   - Filtering Cuisine data:
     - Integrated All Cuisine with frequency < 200 into One called 'Mixed'
   - Ensures focus on major dining locations
   - Standardizing data formats
   - Basic data validation checks

2. **Consumer Data Cleaning**
   - Handling missing values
   - Basic data validation
   - Standardizing formats

### Preprocessing Steps (`/notebooks/recommendation.ipynb`)

1. **Feature Engineering**
   - Encoding categorical variables:
     - Cuisine types
     - Restaurant locations
     - Price ranges
     - Alcohol service options
     - Parking availability
   
   - Processing numerical features:
     - Overall ratings
     - Food ratings
     - Service ratings

2. **Data Integration**
   - Merging cleaned consumer and restaurant data
   - Creating feature matrices for recommendation system

3. **Data Transformation**
   - One-hot encoding for categorical variables
   - Min-Max scaling for numerical features

### Key Data Processing Steps
- Filled missing values in dataset
- Removed low-frequency cities (threshold: 200)
- Standardized categorical variables
- Scaled numerical features
- Integrated multiple data sources

This preprocessing ensures:
1. Clean, consistent data
2. Focus on significant locations
3. Standardized feature format
4. Reliable recommendation results

## 🔠 Technologies Used
- **Programming Language**: Python
- **Framework**: Streamlit
- **Libraries**: Pandas, NumPy, Scikit-learn
- **Tools**: Jupyter Notebooks

## 📊 Data Files Description

1. **Consumer Data**
   - `consumers.csv`: User details.
   - `consumer_preferences.csv`: User preference metrics.
   - `ratings.csv`: User ratings for restaurants.

2. **Restaurant Data**
   - `restaurants.csv`: Restaurant details.
   - `restaurant_cuisines.csv`: Available cuisines.

## 🚀 Getting Started

### **Setup**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the application:
   ```bash
   streamlit run src/app.py
   ```

### **Features**
- **Interactive Web Interface**
  - User-friendly design for seamless interaction.
- **Personalized Recommendations**
  - Tailored suggestions based on user preferences.
- **Filters**
  - Filter by cuisine, location, price, alcohol service, and parking availability.
- **Accurate Recommendations**
  - Rating-based and preference-aligned suggestions.

## 🔄 Data Processing Flow
1. Collect raw data.
2. Clean and preprocess datasets using Jupyter notebooks.
3. Engineer features for better recommendations.
4. Implement the recommendation logic.
5. Integrate with a Streamlit frontend.

## Results
Result 1:![image](https://github.com/user-attachments/assets/edcce333-1046-4740-81f1-18fd34e6a8f4)

Result 2:![image](https://github.com/user-attachments/assets/01e4f18a-466f-4487-9a46-d5f50cdf58b8)

Result 3:![image](https://github.com/user-attachments/assets/6d43a1c3-7398-4371-97d0-14d5f1c61d81)

## 🤝 Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m 'Add feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Open a pull request.

For major changes, kindly open an issue for discussion beforehand.

---

Happy coding! 😊
