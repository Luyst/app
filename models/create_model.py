import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load Data
df = pd.read_csv('models/marketing_campaign.csv', delimiter='\t')
df = df.dropna()

df['Age'] = 2021 - df['Year_Birth']

# Add new columns
df['Kids'] = df['Kidhome'] + df['Teenhome']
df['Expenses'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']

# Replace marital status values
df['Marital_Status'] = df['Marital_Status'].replace({
    'Married': 'In relationship', 'Together': 'In relationship',
    'Divorced': 'Single', 'Widow': 'Single', 'Absurd': 'Single',
    'Alone': 'Single', 'YOLO': 'Single'
})

# Label encode marital status
df['Marital_Status'] = df['Marital_Status'].map({'In relationship': 1, 'Single': 0})

# Replace education values
df['Education'] = df['Education'].replace('2n Cycle', 'Master')

# Label encode education
education_mapping = {
    'Graduation': 1,
    'PhD': 2,
    'Master': 3,
    'Basic': 0
}
df['Education'] = df['Education'].map(education_mapping)

# Drop unused columns
df = df.drop(columns=[
    'ID', 'Year_Birth', 'Dt_Customer', 'Kidhome', 'Teenhome', 'Recency', 
    'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 
    'NumStorePurchases', 'NumWebVisitsMonth', 'AcceptedCmp1', 'AcceptedCmp2', 
    'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Complain', 'Response', 
    'Z_CostContact', 'Z_Revenue'
])

# Rename columns
df.columns = ['Education', 'Marital_Status', 'Income', 'Wines', 'Fruits', 'Meat', 'Fish', 'Sweet', 'Gold', 'Age', 'Children', 'Expenses']

# Create a DataFrame subset for outlier detection
df_subset = df[['Income', 'Age']]

# Calculate z-scores
from scipy import stats
z_scores = np.abs(stats.zscore(df_subset))

# Filter entries with z-scores within [-3, 3]
filtered_entries = (z_scores < 3).all(axis=1)

# Create a new DataFrame with filtered entries
df1 = df[filtered_entries]
df1.reset_index(inplace=True, drop=True)

# Create a scaler and scale the data
scaler = MinMaxScaler()
df1_scaled = scaler.fit_transform(df1)
df1_scaled = pd.DataFrame(df1_scaled, columns=df1.columns)

# KMeans Clustering with k=4
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(df1_scaled)

# Dự đoán cụm cho từng điểm dữ liệu
clusters = kmeans.predict(df1_scaled)

# Thêm cột cluster vào DataFrame df1
df1['Cluster'] = clusters

# Phân tích đặc trưng của các cụm
cluster_features = df1.groupby('Cluster').mean()

# In ra thông tin về đặc trưng của các cụm
print(cluster_features)

for cluster_id, cluster_data in cluster_features.iterrows():
    print(f"Cluster: {cluster_id}")
    top_products = cluster_data[['Wines', 'Fruits', 'Meat', 'Fish', 'Sweet', 'Gold']].nlargest(3)
    print(f"Top 3 Products: {top_products.index.tolist()}\n")


# # Save the model and scaler
joblib.dump(kmeans, 'models/test_model.joblib')
joblib.dump(scaler, 'models/test_scaler.joblib')


# Test mô hình
sample = np.array([[1, 0, 580000, 250, 30, 50, 20, 10, 5, 45, 2, 365]])  # Ví dụ dữ liệu
sample_scaled = scaler.transform(sample)
cluster = kmeans.predict(sample_scaled)

print("Cluster: ", cluster)