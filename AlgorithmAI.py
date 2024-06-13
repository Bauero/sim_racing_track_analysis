import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the CSV file with specific columns and rows
csv_file_path = '13-37-41_29-05-2024_cleaned_data.csv'  # Replace with your file path
selected_columns = ['Section','Time', 'Time_on_lap', 'STEERANGLE', 'THROTTLE', 'RPMS', 'G_LAT', 'G_LON' , 'SPEED', 'BRAKE', 'LAP_BEACON']  # Replace with your specific columns
data = pd.read_csv(csv_file_path, usecols=selected_columns, nrows=200000)


# Further filter rows based on conditions (e.g., rows where 'column1' > 0)
filtered_data = data[data['Section'] == 1]

# Aggregate the data to form single points, e.g., group by a specific column and take the mean
aggregated_data = filtered_data.groupby('LAP_BEACON').mean()  # Replace 'column1' with your grouping column

# Display the first few rows of the aggregated dataframe
print(aggregated_data.head())

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(aggregated_data)

# Apply K-Means Clustering
kmeans = KMeans(n_clusters=4, n_init=10, max_iter=300, random_state=42)
kmeans.fit(scaled_data)
y_kmeans = kmeans.predict(scaled_data)

# Add the cluster assignment to the original dataframe
aggregated_data['Cluster'] = y_kmeans

# Display the first few rows of the dataframe with the cluster assignment
print(aggregated_data.head())

# Reduce dimensions for visualization using PCA
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

# Plot the clusters
plt.figure(figsize=(10, 7))
plt.scatter(pca_data[:, 0], pca_data[:, 1], c=y_kmeans, s=50, cmap='viridis')

# Plot the cluster centers
centers = kmeans.cluster_centers_
pca_centers = pca.transform(centers)
plt.scatter(pca_centers[:, 0], pca_centers[:, 1], c='red', s=200, alpha=0.75, marker='X')
plt.title('K-Means Clustering with PCA')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()
