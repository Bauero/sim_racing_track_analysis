import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from os.path import isfile, dirname
from constants import sign


def train_algorithm(data : pd.DataFrame,
                    section : int = 1, 
                    groupbycol : list = ['LAP_BEACON', 'LAP_NO'], 
                    aggbycol : list = ['Time_on_lap', 'SPEED'],
                    debug : bool = False):
    """
    This code is responsible for creating clusters based on provided data for
    specific section.

    - `data` - data table which will be used for clustering and fruther data 
    processing

    - `section` - clustering is always done for one specific section - here you
    pass number with section for which clustering will be done - by default = 1

    - `groupbycol` - here, you pass list of columns which will be used to split
    data into separate sets - by desigh it should be `LAP_BEACON`, `LAP_NO`

    - `aggbycol` - here you can decide what would be the axis of the graph which
    will be the end result of algorithm
    """
    
    # Restructure data, by filtering and grouping according to input params
    filtered_data = data[data['Section'] == section]
    grouped_data = filtered_data.groupby(groupbycol)
    last_time_on_lap = grouped_data['Time_on_lap'].last()
    aggregated_data = grouped_data.mean()

    # Readjust restructurized data for trainging
    aggregated_data['Time_on_lap'] = last_time_on_lap
    aggregated_data.reset_index(inplace = True)

    if debug:   print(aggregated_data.head())

    # Scale readjusted data, to remove weigh inbalace across columns
    features_to_scale = aggregated_data.drop(columns = aggbycol)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features_to_scale)
    scaled_data = np.hstack((aggregated_data[aggbycol].values, 
                             scaled_features))
    
    # Actual clustering
    kmeans = KMeans(n_clusters=3, n_init=10, max_iter=300, random_state=42)
    kmeans.fit(scaled_data)
    
    # Prediction, and saving the results
    y_kmeans = kmeans.predict(scaled_data)
    aggregated_data['Cluster'] = y_kmeans

    if debug:   print(aggregated_data.head())

    return aggregated_data, kmeans


def plot_group_of_points(aggregated_data, kmeans):
    """
    This function plots all datapoints from the oryginal data, along with all
    markers of the cluster centers
    """

    # Prepare list of points, which mark centers of cluster
    centers = kmeans.cluster_centers_
    center_times = centers[:, 0]
    center_speeds = centers[:, 1]

    y_kmeans = aggregated_data['Cluster']

    # Prepare the plot
    plt.figure(figsize=(10, 7))
    plt.title('K-Means Clustering: Time_on_lap vs. SPEED')
    plt.xlabel('Time on Lap')
    plt.ylabel('Speed')

    # Put points on the plot
    plt.scatter(aggregated_data['Time_on_lap'], 
                aggregated_data['SPEED'], c=y_kmeans, s=50, cmap='viridis')
    plt.scatter(center_times, center_speeds, c='red',
                s=200, alpha=0.75, marker='X')
    plt.show()


def plot_points_from_new_data_with_all_points(new_x_points,
                                              new_y_poinst,
                                              color_new_point,
                                              size_new_point,
                                              aggregated_data,
                                              kmeans):
    """
    By design, this function does mostly the same as the `plot_group_of_points`;
    The only difference, it that it allows to put another set of point, on top
    of the points from aggregated data, for example, to allow to display points
    from the last performace of the player, on to po of the point from statictic
    preformace in history
    """

    plt.ion()
    plot_group_of_points(aggregated_data, kmeans)
    plt.scatter(new_x_points, new_y_poinst, c=color_new_point, s=size_new_point)
    plt.ioff()
    plt.show()


def write_data_into_file(path_to_dir, file_name, aggregated_data, kmeans):
    
    if isfile(path_to_dir):
        path_to_dir = dirname(path_to_dir)

    if not file_name.endswith(".pickle"):
        file_name += ".pickle"

    full_path = path_to_dir + sign + file_name
    
    pickle.dump((aggregated_data, kmeans), open(full_path, "wb"))

    return full_path


def read_data_from_file(path_to_file):

    if not isfile:  return None
    
    if not path_to_file.endswith(".pickle"):    return None

    return pickle.load(open(path_to_file, "rb"))

    
if __name__ == "__main__":

    from tkinter.filedialog import askopenfilename
    from tkinter import Tk
    import pickle

    
    selected_columns = ['Section', 'Time', 'Time_on_lap', 'STEERANGLE', \
                        'THROTTLE','RPMS', 'G_LAT', 'G_LON', 'SPEED', 'BRAKE', \
                        'LAP_BEACON', 'LAP_NO']
    grbycol = ['LAP_BEACON', 'LAP_NO']
    aggbycol = ['Time_on_lap', 'SPEED']

    Tk().withdraw()
    csv_file_path = askopenfilename()  # Replace with your file path
    
    if csv_file_path == "": exit()

    data = pd.read_csv(csv_file_path, usecols=selected_columns)
    aggregated_data, kmeans = train_algorithm(data, 5, grbycol, aggbycol)
    plot_group_of_points(aggregated_data, kmeans)
    
    # Example, on how to use this function
    # plot_points_from_new_data_with_all_points(30,
    #                                           150,
    #                                           'orange',
    #                                           100,
    #                                           aggregated_data,
    #                                           kmeans)
