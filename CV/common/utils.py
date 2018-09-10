import os


def legal_image(image_path):
    if os.path.isfile(image_path):
        filename = os.path.split(image_path)[-1]
        ext = os.path.splitext(filename)[1]
        if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return True
        else:
            print(ext)
            return False
    else:
        return False
