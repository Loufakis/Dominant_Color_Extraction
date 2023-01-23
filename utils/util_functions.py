# Imports
import numpy as np
import cv2
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def load_image(image_path):
    """
    This function takes an image path as input, reads it using OpenCV,
    rescales it so that the width is 250 pixels, converts it to the RGB
    format, and returns the image array.
    
    Parameters:
        image_path (str): The path to the image to be processed.
    
    Returns:
        np.ndarray : The processed image in the form of a numpy array.
    """
    
    # Read Image
    img_array = cv2.imread(image_path)
    
    # Rescale by keeping the analogy between width and height
    img_ratio = img_array.shape[0] / img_array.shape[1]
    new_w, new_h = 250, int(250*img_ratio)
    img_array = cv2.resize(img_array, dsize=(new_w, new_h))
    
    # Convert to RGB format
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    
    return img_array


def color_distance(color1, color2):
    """
    This function takes two colors as input and computes the Euclidean
    distance between them.
    
    Parameters:
        color1 (list[float, float, float]): The first color in the format of (R, G, B)
                                            where R, G and B are floats between 0 and 1.
        color2 (list[float, float, float]): The second color in the format of (R, G, B)
                                            where R, G and B are floats between 0 and 1.
        
    Returns:
        float: The Euclidean distance between the two colors.
    """
    
    return np.linalg.norm(np.array(color1)-np.array(color2))

   
def silhouette_method(color_data):
    """
    This function takes color data in the form of a numpy array and uses the silhouette 
    method to determine the optimal number of clusters in the color space.
    
    Parameters:
        color_data (np.ndarray): The color data to be clustered in the form of a numpy
                                 array with shape (n_samples, n_features) where n_samples
                                 is the number of pixels in the image and n_features is
                                 the number of color channels (usually 3 for RGB or LAB
                                 images)
        
    Returns:
        int: The optimal number of clusters in the color space
    """
    
    # Initialize an empty list to store silhouette scores
    silhouette_scores = []

    # Loop through different numbers of clusters
    for n_clusters in range(2, 10):
        # Create a k-means model with the current number of clusters
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++')
        # Fit the k-means model to the color_data
        kmeans.fit(color_data)
        # Get the silhouette score for the current model
        score = silhouette_score(color_data, kmeans.labels_)
        # Add the silhouette score to the list
        silhouette_scores.append(score)

        # Find the number of clusters with the highest silhouette score
        best_n_clusters = np.argmax(silhouette_scores) + 2
        
        return best_n_clusters


def short_clusters(pixels, cluster_labels):
    """
    This function takes an array of pixel values for an image and a list of cluster
    assignments for each pixel. It returns a dictionary sorted by the number of pixels
    in each cluster, along with the mean color value for each cluster.
    
    Parameters:
    pixels   (np.ndarray): An array containing the pixels of an image.
    cluster_labels (list): A list with the cluster that every pixel belongs.
    
    Returns:
    dict: A dictionary containing the number of pixels in each cluster and the mean
          color value of those pixels.
    """ 
    
    # Create an empty dictionary to store each cluster and the pixels belonging to them
    cluster_data = {}
    # Loop through all image pixels and the corresponding cluster label
    for pxl, cluster in zip(pixels, cluster_labels):
        # Check if the current cluster already belongs to the dictionary
        if cluster not in cluster_data.keys():
            # If the cluster does not belong, add it and stack the first pixel
            cluster_data[cluster] = np.empty((3,))
            cluster_data[cluster] = np.vstack((cluster_data[cluster],pxl))
        else:
            # If the cluster already belongs to the dictionary, just stack the new pixel
            cluster_data[cluster] = np.vstack((cluster_data[cluster],pxl))
    
    # Create an empty list to store for each clusters id the number of pixels and the mean color value     
    clusters = {}
    # Create an empty list to keep track of the pixels count
    counts = []

    # Loop through all clusters and their corresponding pixels
    for cluster, cluster_pixels in cluster_data.items():
        # Add cluster
        clusters[cluster] = {}
        # Compute number of pixels
        clusters[cluster]['pxls_count'] = cluster_pixels.shape[0]
        # Compute mean color value
        clusters[cluster]['mean_lab'  ] = cluster_pixels.mean(axis=0)
        # Track pixels
        counts.append(clusters[cluster]['pxls_count'])
        
    # Sort the clusters by their pixels count
    clusters = dict(sorted(clusters.items(), key=lambda item: item[1]["pxls_count"], reverse=True))

    return clusters


if __name__ == "__main__":
    pass