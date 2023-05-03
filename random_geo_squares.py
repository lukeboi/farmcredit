import random
import json
from nltk.corpus import wordnet
import math

# Define the number of shapes to generate
num_shapes = 55000

# Define the range of coordinates for the center of each shape
lat_range = (37.0, 45.5)
lon_range = (-100.0, -90.0)

# Define the range of side lengths for each shape
side_length_range = (0.001, 0.01)

# Define a list of random adjectives and nouns for the shapes
adjectives = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black', 'white']
nouns = ['apple', 'banana', 'car', 'dog', 'elephant', 'fish', 'guitar', 'hat', 'igloo', 'jacket', 'kangaroo', 'lion', 'mountain', 'ninja', 'ocean', 'penguin', 'queen', 'robot', 'shark', 'tree', 'unicorn', 'vampire', 'whale', 'xylophone', 'yacht', 'zebra']

# Define an empty list to hold the GeoJSON features
features = []

def rotate_point(cx, cy, x, y, cos_theta, sin_theta):
    """
    Rotate a point around the center point (cx, cy) by an angle theta
    """
    nx = cos_theta * (x - cx) - sin_theta * (y - cy) + cx
    ny = sin_theta * (x - cx) + cos_theta * (y - cy) + cy
    return (nx, ny)

# Generate the GeoJSON features
for i in range(num_shapes):
    # Generate random coordinates for the center of the shape
    center_lon = random.uniform(*lon_range)
    center_lat = random.uniform(*lat_range)
    
    # Generate a random side length for the shape
    side_length = random.uniform(*side_length_range)
    
    # Generate a random rotation angle for the shape
    rotation_angle = random.uniform(0, 360)
    
    # Calculate the coordinates of the corners of the shape
    half_side = side_length / 2
    top_left = (center_lon - half_side, center_lat + half_side)
    top_right = (center_lon + half_side, center_lat + half_side)
    bottom_right = (center_lon + half_side, center_lat - half_side)
    bottom_left = (center_lon - half_side, center_lat - half_side)
    
    # Rotate the coordinates of the corners
    rotation_angle_rad = rotation_angle * (2 * 3.14159 / 360)
    cos_theta = round(math.cos(rotation_angle_rad), 5)
    sin_theta = round(math.sin(rotation_angle_rad), 5)
    top_left = rotate_point(center_lon, center_lat, top_left[0], top_left[1], cos_theta, sin_theta)
    top_right = rotate_point(center_lon, center_lat, top_right[0], top_right[1], cos_theta, sin_theta)
    bottom_right = rotate_point(center_lon, center_lat, bottom_right[0], bottom_right[1], cos_theta, sin_theta)
    bottom_left = rotate_point(center_lon, center_lat, bottom_left[0], bottom_left[1], cos_theta, sin_theta)
    
    # Define the GeoJSON feature for the shape
    feature = {
        'type': 'Feature',
        'properties': {
            'name': random.choice(adjectives) + random.choice(nouns) + " " + str(i),
            'category': 'default',
            'shape': 'Polygon'
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': [[
                [top_left[0], top_left[1]],
                [top_right[0], top_right[1]],
                [bottom_right[0], bottom_right[1]],
                [bottom_left[0], bottom_left[1]],
                [top_left[0], top_left[1]]
            ]]
        },
        'id': i+1
    }
    
    # Add the feature to the list of features
    features.append(feature)

# Define the GeoJSON feature collection
feature_collection = {
    'type': 'FeatureCollection',
    'features': features
}

# Write the GeoJSON feature collection to a file
with open('static/geo.geojson', 'w') as f:
    json.dump(feature_collection, f)
