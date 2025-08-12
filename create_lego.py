import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import random

from colors import LEGO_COLORS

def closest_color(rgb):
    return min(LEGO_COLORS.items(), key=lambda x: sum((int(a) - int(b)) ** 2 for a, b in zip(rgb, x[1])))


def color_quantization(image, n_colors=24):
    pixels = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels)
    palette = kmeans.cluster_centers_.astype(int)
    quantized = palette[labels].reshape(image.shape)
    return quantized


def create_lego_mosaic(image_path, brick_types, brick_size=8):
    print("Reading image...")
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize image to fit brick sizes
    print("Resizing...")
    h, w = img.shape[:2]
    new_h = (h // brick_size) * brick_size
    new_w = (w // brick_size) * brick_size
    img = cv2.resize(img, (new_w, new_h))

    print("Applying color quantization...")
    img_quantized = color_quantization(img)

    mosaic = np.zeros((new_h, new_w, 3), dtype=np.uint8)

    print("Map to brick types...")
    for y in range(0, new_h, brick_size):
        for x in range(0, new_w, brick_size):
            brick_type = random.choice(brick_types)
            brick_h, brick_w = brick_type

            if y + brick_h * brick_size <= new_h and x + brick_w * brick_size <= new_w:
                brick_area = img_quantized[y:y + brick_h * brick_size, x:x + brick_w * brick_size]
                avg_color = np.mean(brick_area, axis=(0, 1)).astype(int)
                lego_color_name, lego_color = closest_color(avg_color)

                cv2.rectangle(mosaic, (x, y), (x + brick_w * brick_size - 1, y + brick_h * brick_size - 1), lego_color,
                              -1)
                cv2.rectangle(mosaic, (x, y), (x + brick_w * brick_size - 1, y + brick_h * brick_size - 1),
                              (max(0, lego_color[0] - 30), max(0, lego_color[1] - 30), max(0, lego_color[2] - 30)), 1)

                for by in range(brick_h):
                    for bx in range(brick_w):
                        stud_x = x + bx * brick_size + brick_size // 2
                        stud_y = y + by * brick_size + brick_size // 2
                        cv2.circle(mosaic, (stud_x, stud_y), brick_size // 4, (
                        min(lego_color[0] + 30, 255), min(lego_color[1] + 30, 255), min(lego_color[2] + 30, 255)), -1)
                        cv2.circle(mosaic, (stud_x, stud_y), brick_size // 4,
                                   (max(0, lego_color[0] - 30), max(0, lego_color[1] - 30), max(0, lego_color[2] - 30)),
                                   1)

    return mosaic

def show_image(lego_mosaic, width=7, height=7):
    plt.figure(figsize=(width, height))
    plt.imshow(lego_mosaic)
    plt.axis('off')
    plt.title('LEGO Mosaic')
    plt.show()

