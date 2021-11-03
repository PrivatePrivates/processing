import random
import tensorflow_hub as hub
import tensorflow as tf
from flask import Flask, request
import numpy as np
from PIL import Image, ImageOps
from scipy.spatial import cKDTree
from skimage.feature import plot_matches
from skimage.measure import ransac
from skimage.transform import AffineTransform
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)

resultFolder = "results"

delf = hub.load('https://tfhub.dev/google/delf/1').signatures['default']
print("Model Ready!")
os.makedirs(resultFolder, exist_ok=True)


def run_delf(image):
    np_image = np.array(image)
    float_image = tf.image.convert_image_dtype(np_image, tf.float32)

    return delf(
        image=float_image,
        score_threshold=tf.constant(100.0),
        image_scales=tf.constant(
            [0.25, 0.3536, 0.5, 0.7071, 1.0, 1.4142, 2.0]),
        max_feature_num=tf.constant(1000))


def load_and_resize(name, new_width=256, new_height=256):
    image = Image.open(name)
    image = ImageOps.fit(image, (new_width, new_height), Image.ANTIALIAS)
    return image


def match_images(image1, image2, result1, result2):
    distance_threshold = 0.8

    # Read features.
    num_features_1 = result1['locations'].shape[0]
    print("Loaded image 1's %d features" % num_features_1)

    num_features_2 = result2['locations'].shape[0]
    print("Loaded image 2's %d features" % num_features_2)

    # Find nearest-neighbor matches using a KD tree.
    d1_tree = cKDTree(result1['descriptors'])
    _, indices = d1_tree.query(
        result2['descriptors'],
        distance_upper_bound=distance_threshold)

    # Select feature locations for putative matches.
    locations_2_to_use = np.array([
        result2['locations'][i, ]
        for i in range(num_features_2)
        if indices[i] != num_features_1
    ])
    locations_1_to_use = np.array([
        result1['locations'][indices[i], ]
        for i in range(num_features_2)
        if indices[i] != num_features_1
    ])

    # Perform geometric verification using RANSAC.
    _, inliers = ransac(
        (locations_1_to_use, locations_2_to_use),
        AffineTransform,
        min_samples=3,
        residual_threshold=20,
        max_trials=1000)

    print('Found %d inliers' % sum(inliers))

    # Visualize correspondences.
    fig, ax = plt.subplots()
    inlier_idxs = np.nonzero(inliers)[0]
    plot_matches(
        ax,
        image1,
        image2,
        locations_1_to_use,
        locations_2_to_use,
        np.column_stack((inlier_idxs, inlier_idxs)),
        matches_color='b')
    ax.axis('off')
    ax.set_title('Connections between images')


@app.route("/", methods=["POST"])
def compare_images():
    image1 = load_and_resize(request.json["image1"])
    image2 = load_and_resize(request.json["image2"])

    result1 = run_delf(image1)
    result2 = run_delf(image2)

    match_images(image1, image2, result1, result2)
    filename = f"res-{random.randrange(1, 100)}.jpg"
    plt.savefig(f"{resultFolder}/{filename}")
    return f"{filename}!\n"
