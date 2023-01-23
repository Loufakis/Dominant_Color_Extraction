# Imports
import numpy as np
import json
import skimage 
import matplotlib.pyplot as plt
from utils.util_functions import color_distance


class Color():
    """
    This class represents a color and takes as input the color value in a list with three
    values and a string to specify the color format (RGB/LAB) when instantiated.

    Attributes:
    rgb (list): A list of three float values representing the color in the RGB format,
                with values from 0 to 1.
    lab (list): A list of three float values representing the color in the LAB format.
    name (str): The name of the color.

    Methods:
    plot(): Prints the color with a colored square.
    """
    
    def __init__(self, color_values, color_format='rgb'):
        """
        Initializes the Color class with color values and a color format.
        
        Parameters:
        color_values (list): A list of three float values representing the color.
        color_format (str): The color format, either "RGB" or "LAB".
        """
        
        # Check if the given color is in RGB format, if so compute also the LAB
        # format and store the values
        if color_format == 'rgb':
            self.rgb = color_values
            self.lab = skimage.color.rgb2lab(color_values)
        
        # Check if the given color is in LAB format, if so compute also the RGB
        # format and store the values   
        elif color_format == 'lab':
            self.lab = color_values
            self.rgb = skimage.color.lab2rgb(color_values)
        
        # Read the saved .json file witch contains the color names and their value in LAB format    
        with open('Color_Dicts/lab_colors.json') as f:
            LAB_COLORS = json.load(f)
        
        # Find Optimal color name (closest to the one given)
        min_dist = np.inf
        optimal_name = None
        
        # Loop through all the LAB color names and their value   
        for color_name, lab_vector in LAB_COLORS.items():
            # Calculate the distance of the current color and from the one given
            current_dist = color_distance(self.lab, lab_vector)
            
            # If this color is closest as the one already stored, replace
            if current_dist < min_dist:
                min_dist = current_dist
                optimal_name = color_name
        
        # Save the color name       
        self.name = optimal_name
     
    def plot(self):
        """
        Prints the color with a colored square.
        """
        # Create a image figure
        plt.imshow([[self.rgb]])
        
        # Add a title
        plt.title(self.name)
        
        # Display the figure
        plt.show()


class Palette():
    """"
    This class represents a color palette and takes as input a list of colors when
    instantiated, which are instances of the 'Color' class.
    
    Attributes:
    names (list): A list of strings representing the names of the colors in the palette.
    rgb   (list): A list of lists of three float values representing the color values in
                  the RGB format for the colors in the palette.
    lab   (list): A list of lists of three float values representing the color values in
                  the LAB format for the colors in the palette.

    Methods:
    plot(): Prints the palette.
    """
    
    def __init__(self, colors):
        """
        Initializes the Palette class with a list of color instances.
        
        Parameters:
        colors (list): A list of instances of the 'Color' class.
        """
        
        # Create an empry list for all three attributes
        self.names = []
        self.rgb   = []
        self.lab   = []
        
        # Loop through all colors and append their attributes to
        # the empty lists
        for color in colors:
            self.names.append(color.name)
            self.rgb.append(color.rgb)
            self.lab.append(color.lab)
    
    def plot(self):
        """
        Prints the palette.
        """
        
        # Create a figure and a subplot
        fig, ax = plt.subplots()

        # Add a rectangle for each color in the palette
        for idx, color in enumerate(self.rgb):
            ax.add_patch(plt.Rectangle((idx, 0), 1, 1, color=color))
        
        # Add a title
        ax.set_title('Dominant Colors')
          
        # Set the x-axis tick labels to the labels for the colors
        ax.set_xticks([i + 0.5 for i in range(len(self.rgb))]+[idx+1])
        ax.set_xticklabels(self.names+[''], rotation = 45)

        # Remove the y-axis and grid
        ax.set_yticks([])
        ax.grid(False)

        # Display the figure
        plt.show()


if __name__ == "__main__":
    pass