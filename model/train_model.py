import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load the new dataset
df = pd.read_csv('data/Mental Health Dataset.csv')

# Drop irrelevant columns
df = df.drop(columns=['Timestamp', 'Country', 'Occupation', 'self_employed', 'Gender'])

# Simple imputation for missing values - assuming 'Yes'/'No' or similar categorical data
for col in df.select_dtypes(include=['object']).columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Create a 'risk_label' based on 'Coping_Struggles'
# Assuming 'Yes' indicates a struggle and therefore a risk
df['risk_label'] = df['Coping_Struggles'].apply(lambda x: 1 if x == 'Yes' else 0)

# Encode categorical variables
for column in df.columns:
    if df[column].dtype == 'object':
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])

# Define features (X) and target (y)
X = df.drop('risk_label', axis=1)
y = df['risk_label']

# Store feature columns to ensure prediction input matches
feature_columns = X.columns.tolist()

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model and feature list
with open('model/rf_model.pkl', 'wb') as model_file:
    pickle.dump({'model': model, 'features': feature_columns}, model_file)

print("Model trained and saved successfully with the new dataset.")