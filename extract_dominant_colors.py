# Imports
import argparse
from skimage import color
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from utils.util_functions import load_image, silhouette_method, short_clusters
from utils.util_classes import Color, Palette


def extract_dominant_colors(img_path, number_of_colors):
    """
    This function takes an image path and a number of colors as input,
    then uses the KMeans algorithm to extract the specified number of
    dominant colors from the image. If no number of colors is specified,
    it uses the silhouette method to determine the optimal number of
    colors to extract. Finally, it prints the dominant colors.
    
    Parameters:
        img_path (str): The path to the image from which to extract colors.
        number_of_colors (int): The number of dominant colors to extract from the image.
                                Default is None.
        
    Returns:
        None
    """
    
    # 1. Load the image
    img_arr = load_image(img_path) # Here the image is in RGB format with values in [0, 255]
    # Get a look at the imported image
    plt.imshow(img_arr)
    plt.title('Imported Image')
    plt.xticks([])
    plt.yticks([])
    plt.show()
    
    # 2. Convert image array from RGB to LAB format
    # but first we must convert the RGB scale from [0,255] to [0,1]
    img_arr = img_arr/255
    # Now convert to LAB format
    img_arr_lab = color.rgb2lab(img_arr) 
    
    # 3. Reshape
    # Reshape to (height*width, channels) = (..., 3). Because the K-Means need a 2D Array as input
    img_vec = img_arr_lab.reshape((img_arr_lab.shape[0]*img_arr_lab.shape[1],3))
    
    # 4. Defeine number of colors to extract
    if not number_of_colors: # Check if number_of_colors == None
        # Because the number of colors isn't defeined we use the 
        # silhouette method to defeine the optimal number
        print('Choosing the optimal number of colors to extract.')
        print('Waiting for the silhouette method to converge...')
        number_of_colors = silhouette_method(img_vec)
       
    # 5. Apply Clustering   
    kmeans = KMeans(n_clusters=number_of_colors, init='k-means++')
    kmeans.fit(img_vec)
    
    # 6. Short extracted colors by their pixel count in the image
    clusters = short_clusters(img_vec, kmeans.labels_)

    # 7. Plot Extracted Palette
    # Create an Empty color list
    colors = []
    # Loop through all clusters
    for cluster in clusters.keys():
        # Use each cluster mean LAB value to defeine an instance of the class 'Color'
        # and append all colors to the colors list
        colors.append(Color(clusters[cluster]['mean_lab'], color_format='lab'))
    # Use the list of colors to defeine a class 'Palette'    
    extracted_colors = Palette(colors)
    # Print the extracted colors
    print('And the dominant colors are:')
    extracted_colors.plot()
    
        
if __name__ == "__main__":
    # Defeine the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required=True, help="path to the image file")
    parser.add_argument("-c", "--clusters", default=None, type=int, help="number of clusters/colors to extract")
    args = parser.parse_args()
    # Apply the color extraction function
    extract_dominant_colors(args.image, args.clusters)