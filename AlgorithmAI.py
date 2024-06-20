import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from tkinter.filedialog import askopenfilename
from tkinter import Tk

# Load the CSV file with specific columns
# Tk.withdraw()
csv_file_path = askopenfilename()  # Replace with your file path
selected_columns = ['Section', 'Time', 'Time_on_lap', 'STEERANGLE', 'THROTTLE', 'RPMS', 'G_LAT', 'G_LON', 'SPEED', 'BRAKE', 'LAP_BEACON', 'LAP_NO']
data = pd.read_csv(csv_file_path, usecols=selected_columns, nrows=5000000)

# Filter the data to only include rows where Section == 1
filtered_data = data[data['Section'] == 5]

# Group the data by 'LAP_BEACON' and 'id', then get the last 'Time_on_lap' for each group
last_time_on_lap = filtered_data.groupby(['LAP_BEACON', 'LAP_NO'])['Time_on_lap'].last()

# Aggregate other features by mean
aggregated_data = filtered_data.groupby(['LAP_BEACON', 'LAP_NO']).mean()

# Replace the aggregated 'Time_on_lap' with the last 'Time_on_lap'
aggregated_data['Time_on_lap'] = last_time_on_lap

# Reset index to flatten the DataFrame
aggregated_data.reset_index(inplace=True)

# Display the first few rows of the aggregated dataframe
print(aggregated_data.head())

# Standardize the data except for 'Time_on_lap' and 'SPEED'
features_to_scale = aggregated_data.drop(columns=['Time_on_lap', 'SPEED'])
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features_to_scale)

# Combine scaled features with 'Time_on_lap' and 'SPEED'
scaled_data = np.hstack((aggregated_data[['Time_on_lap', 'SPEED']].values, scaled_features))

# Apply K-Means Clustering
kmeans = KMeans(n_clusters=3, n_init=10, max_iter=300, random_state=42)
kmeans.fit(scaled_data)
y_kmeans = kmeans.predict(scaled_data)

# Add the cluster assignment to the aggregated dataframe
aggregated_data['Cluster'] = y_kmeans

# Display the first few rows of the dataframe with the cluster assignment
print(aggregated_data.head())

# Plot the clusters with 'Time_on_lap' on the x-axis and 'SPEED' on the y-axis
plt.figure(figsize=(10, 7))
plt.scatter(aggregated_data['Time_on_lap'], aggregated_data['SPEED'], c=y_kmeans, s=50, cmap='viridis')

# Plot the cluster centers
centers = kmeans.cluster_centers_
# Extract the 'Time_on_lap' and 'SPEED' for the cluster centers
center_times = centers[:, 0]
center_speeds = centers[:, 1]
plt.scatter(center_times, center_speeds, c='red', s=200, alpha=0.75, marker='X')
plt.title('K-Means Clustering: Time_on_lap vs. SPEED')
plt.xlabel('Time on Lap')
plt.ylabel('Speed')
plt.show()