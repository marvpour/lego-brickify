from create_lego import create_lego_mosaic, show_image

if __name__ == '__main__':
    BRICK_TYPES = [(1, 4),
                   (2, 4),
                   (2, 6),
                   (2, 1)]

    image_path = "/home/maryam/Desktop/my_image.jpg"
    lego_mosaic = create_lego_mosaic(image_path)
    show_image(lego_mosaic)