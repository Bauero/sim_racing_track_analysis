import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from os.path import isfile, dirname


def process_grouped_data(grouped_data, col, process_type):
    match process_type:
        case 'highest':
            return grouped_data[col].apply(lambda x: x.loc[x.abs().idxmax()])
        case 'last':
            return grouped_data[col].last()
        case 'average':
            return grouped_data[col].mean()
        case _:
            return grouped_data[col]


def train_algorithm(data : pd.DataFrame,
                    section : int = 1, 
                    groupbycol : list = ['LAP_BEACON', 'LAP_NO'], 
                    col1: str = 'Distance_on_lap',
                    col2: str = 'BRAKE',
                    col1_process: str = 'none',
                    col2_process: str = 'none',
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

    if debug:
        print("Filtered Data:")
        print(filtered_data.head())

    if col1_process != 'none':
        aggregated_col1 = process_grouped_data(grouped_data, 
                                               col1, 
                                               col1_process).reset_index()
    else:
        aggregated_col1 = filtered_data[[groupbycol[0], 
                                         groupbycol[1], 
                                         col1]].copy()
        
    if col2_process != 'none':
        aggregated_col2 = process_grouped_data(grouped_data, 
                                               col2, 
                                               col2_process).reset_index()
    else:
        aggregated_col2 = filtered_data[[groupbycol[0], 
                                         groupbycol[1], 
                                         col2]].copy()
    
    # If either col1_process or col2_process is 'none', we need to handle it differently
    if col1_process == 'none' and col2_process == 'none':
        aggregated_data = filtered_data[[groupbycol[0], 
                                         groupbycol[1], 
                                         col1, 
                                         col2]].copy()
    elif col1_process == 'none':
        aggregated_data = pd.merge(aggregated_col1, 
                                   aggregated_col2, 
                                   on=groupbycol, 
                                   suffixes=('_col1', '_col2'))
        aggregated_data.rename(columns={f'{col2}_col2': col2}, inplace=True)
    
    elif col2_process == 'none':
        aggregated_data = pd.merge(aggregated_col1, 
                                   aggregated_col2, 
                                   on=groupbycol, 
                                   suffixes=('_col1', '_col2'))
        aggregated_data.rename(columns={f'{col1}_col1': col1}, inplace=True)

    else:
        aggregated_data = pd.merge(aggregated_col1, 
                                   aggregated_col2, 
                                   on=groupbycol, 
                                   suffixes=('_col1', '_col2'))
        aggregated_data.rename(columns={f'{col1}_col1': col1, 
                                        f'{col2}_col2': col2}, inplace=True)

    if debug:
        print("Aggregated Data:")
        print(aggregated_data.head())

    # Ensure that only numerical columns are scaled
    features_to_scale = aggregated_data.drop(columns=[col1, col2], 
                                             errors='ignore')
    if not features_to_scale.empty:
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features_to_scale)
        scaled_data = np.hstack((aggregated_data[[col1, col2]].values, 
                                 scaled_features))
    else:
        scaled_data = aggregated_data[[col1, col2]].values

    if debug:
        print("Scaled Data:")
        print(scaled_data[:5])

    # Actual clustering
    kmeans = KMeans(n_clusters=3, n_init=10, max_iter=300, random_state=42)
    kmeans.fit(scaled_data)
    
    # Prediction, and saving the results
    y_kmeans = kmeans.predict(scaled_data)
    aggregated_data['Cluster'] = y_kmeans

    if debug:   
        print("Final Aggregated Data with Clusters:")
        print(aggregated_data.head())

    return aggregated_data, kmeans


def filter_data(data : pd.DataFrame, 
                section : int = 1, 
                groupbycol : list = ['LAP_BEACON', 'LAP_NO'],
                col1: str = 'Distance_on_lap',
                col2: str = 'BRAKE',
                col1_process: str = 'none',
                col2_process: str = 'none',
                debug : bool = False):
    
    """
    
    - col1 / col2 _process - options: 'average', 'last', 'highest', 'none'
    """

    # Restructure data, by filtering and grouping according to input params
    filtered_data = data[data['Section'] == section]
    grouped_data = filtered_data.groupby(groupbycol)
    
    if debug:
        print("Filtered Data:")
        print(filtered_data.head())

    if col1_process != 'none':
        aggregated_col1 = process_grouped_data(grouped_data, 
                                               col1, 
                                               col1_process).reset_index()
    else:
        tmp = groupbycol + [col1]
        aggregated_col1 = filtered_data[tmp].copy()
        
    if col2_process != 'none':
        aggregated_col2 = process_grouped_data(grouped_data, 
                                               col2, 
                                               col2_process).reset_index()
    else:
        tmp = groupbycol + [col2]
        aggregated_col2 = filtered_data[tmp].copy()
    
    # If either col1_process or col2_process is 'none', 
    # we need to handle it differently
    if col1_process == 'none' and col2_process == 'none':
        tmp = groupbycol + [col1, col2]
        aggregated_data = filtered_data[tmp].copy()

    elif col1_process == 'none':
        aggregated_data = pd.merge(aggregated_col1, 
                                   aggregated_col2, 
                                   on = groupbycol, 
                                   suffixes = ('_col1', '_col2'))
        aggregated_data.rename(columns={f'{col2}_col2': col2}, inplace=True)

    elif col2_process == 'none':
        aggregated_data = pd.merge(aggregated_col1, 
                                   aggregated_col2, 
                                   on = groupbycol, 
                                   suffixes = ('_col1', '_col2'))
        aggregated_data.rename(columns={f'{col1}_col1': col1}, inplace=True)

    else:
        aggregated_data = pd.merge(aggregated_col1, 
                                   aggregated_col2, 
                                   on = groupbycol, 
                                   suffixes=('_col1', '_col2'))
        aggregated_data.rename(columns={f'{col1}_col1': col1, 
                                        f'{col2}_col2': col2}, inplace=True)

    if debug:   
        print("Aggregated Data:")
        print(aggregated_data.head())

    return aggregated_data[[col1, col2]]


def filter_data_oryginal(data : pd.DataFrame, 
                         section : int = 1, 
                         groupbycol : list = ['LAP_BEACON', 'LAP_NO'], 
                         aggbycol : list = ['Time_on_lap', 'SPEED'],
                         debug : bool = False):
    
    # Restructure data, by filtering and grouping according to input params
    filtered_data = data[data['Section'] == section]
    grouped_data = filtered_data.groupby(groupbycol)
    last_time_on_lap = grouped_data['Time_on_lap'].last()
    aggregated_data = grouped_data.mean()

    # Readjust restructurized data for trainging
    aggregated_data['Time_on_lap'] = last_time_on_lap
    aggregated_data.reset_index(inplace = True)

    if debug:   print(aggregated_data.head())

    return aggregated_data[aggbycol]


def plot_group_of_points(aggregated_data, kmeans, section, col1, col2):
    # Prepare list of points, which mark centers of cluster
    centers = kmeans.cluster_centers_
    center_col1 = centers[:, 0]
    center_col2 = centers[:, 1]
    cluster_colors = ['blue', 'green', 'orange', 'purple']

    y_kmeans = aggregated_data['Cluster']

    # Prepare the plot
    plt.figure(figsize=(10, 7))
    plt.title(f'K-Means Clustering: {col1} vs. {col2} - section {section}')
    plt.xlabel(col1)
    plt.ylabel(col2)

    # If custom colors are not provided, use a default colormap
    if cluster_colors is None:
        cmap = plt.get_cmap('viridis')
        cluster_colors = [cmap(i) for i in np.linspace(0, 1, 
                                                       len(np.unique(y_kmeans)))]

    # Plot points with specified colors for each cluster
    unique_clusters = np.unique(y_kmeans)
    for cluster, color in zip(unique_clusters, cluster_colors):
        subset = aggregated_data[aggregated_data['Cluster'] == cluster]
        plt.scatter(subset[col1], subset[col2], color=color, s=50, 
                    label=f'Cluster {cluster}')

    # Plot cluster centers
    plt.scatter(center_col1, center_col2, c='red', s=200, alpha=0.75, 
                marker='X', label='Cluster Centers')

    # Create custom legend handles
    handles = [plt.Line2D([0], [0], marker='o', color='w', 
                          label=f'Cluster {cluster}', 
                          markerfacecolor=color, markersize=10) 
               for cluster, color in zip(unique_clusters, cluster_colors)]

    # Add cluster centers to the legend
    handles.append(plt.Line2D([0], [0], marker='X', color='w', 
                              label='Cluster Centers', 
                              markerfacecolor='red', markersize=10))

    plt.legend(handles=handles)
    
    plt.show()


def plot_points_from_new_data_with_all_points(new_x_points,
                                              new_y_points,
                                              color_new_point,
                                              size_new_point,
                                              aggregated_data,
                                              kmeans,
                                              section,
                                              col1,
                                              col2):
    """
    By design, this function does mostly the same as the `plot_group_of_points`;
    The only difference, it that it allows to put another set of point, on top
    of the points from aggregated data, for example, to allow to display points
    from the last performance of the player, on top of the points from statistic
    performance in history
    """

    centers = kmeans.cluster_centers_
    center_col1 = centers[:, 0]
    center_col2 = centers[:, 1]
    cluster_colors = ['blue', 'green', 'orange', 'purple']

    y_kmeans = aggregated_data['Cluster']

    # Prepare the plot
    plt.figure(figsize=(10, 7))
    plt.title(f'K-Means Clustering: {col1} vs. {col2} - section {section}')
    plt.xlabel(col1)
    plt.ylabel(col2)

    # Plot points with specified colors for each cluster
    unique_clusters = np.unique(y_kmeans)
    for cluster, color in zip(unique_clusters, cluster_colors):
        subset = aggregated_data[aggregated_data['Cluster'] == cluster]
        plt.scatter(subset[col1], subset[col2], color=color, s=50, 
                    label=f'Cluster {cluster}')

    # Plot cluster centers
    plt.scatter(center_col1, center_col2, c='red', s=200, alpha=0.75, 
                marker='X', label='Cluster Centers')

    # Create custom legend handles
    handles = [plt.Line2D([0], [0], marker='o', color='w', 
                          label=f'Cluster {cluster}', 
                          markerfacecolor=color, markersize=10) 
               for cluster, color in zip(unique_clusters, cluster_colors)]

    # Add cluster centers to the legend
    handles.append(plt.Line2D([0], [0], marker='X', color='w', 
                              label='Cluster Centers', 
                              markerfacecolor='red', markersize=10))

    # Plot new user data points
    plt.scatter(new_x_points, new_y_points, c=color_new_point, 
                s=size_new_point, marker='+')

    # Append the new legend entry
    handles.append(plt.Line2D([0], [0], marker='+', color='w', label='User data', 
                              markeredgecolor = color_new_point, markersize=10))
    
    # Update the legend with the new handles
    plt.legend(handles=handles)
    plt.show()


def write_data_into_file(path_to_dir, file_name, 
                         aggregated_data, kmeans, col1, col2):
    
    if isfile(path_to_dir):
        path_to_dir = dirname(path_to_dir)

    if not file_name.endswith(".pickle"):
        file_name += ".pickle"

    full_path = path_to_dir + "/" + file_name
    
    pickle.dump((aggregated_data, kmeans, col1, col2), open(full_path, "wb"))

    return full_path


def read_data_from_file(path_to_file):

    if not isfile:  return None
    
    if not path_to_file.endswith(".pickle"):    return None

    return pickle.load(open(path_to_file, "rb"))

    
if __name__ == "__main__":

    from tkinter.filedialog import askopenfilename
    from tkinter import Tk

    
    selected_columns = ['Section', 'Time', 'Time_on_lap', 'STEERANGLE', \
                        'THROTTLE','RPMS', 'G_LAT', 'G_LON', 'SPEED', 'BRAKE', \
                        'LAP_BEACON', 'LAP_NO', "Distance", "Distance_on_lap"]
    grbycol = ['LAP_BEACON', 'LAP_NO']
    aggbycol = ['Time_on_lap', 'SPEED']
    section = 5
    col1 = aggbycol[0]
    col2 = aggbycol[1]

    processing_option = {
        'SPEED' : 'average',
        'Time_on_lap' : 'last',
        'Distance' : 'none',
        'Distance_on_lap' : 'none',
        'BRAKE' : 'none',
        'STEERANGLE' : 'highiest',
        'THROTTLE' : 'average'
    }

    col1_proc = processing_option[col1]
    col2_proc = processing_option[col2]

    Tk().withdraw()
    csv_file_path = askopenfilename()  # Replace with your file path
    
    if csv_file_path == "": exit()

    data = pd.read_csv(csv_file_path, usecols = selected_columns)
    aggregated_data, kmeans = train_algorithm(data, section, grbycol, 
                                              col1, col2,
                                              col1_process = col1_proc, 
                                              col2_process = col2_proc, 
                                              debug=True)
    plot_group_of_points(aggregated_data, kmeans, section, col1, col2)
