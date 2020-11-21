import os
import os.path
from os import path

from PIL import Image


class ImageUtils:
    img_tmp_directory = "img_tmp"

    @classmethod
    def create_img_tmp_folder(cls):
        if not path.exists(cls.img_tmp_directory):
            os.mkdir(cls.img_tmp_directory)

    @classmethod
    def remove_img_tmp_folder(cls):
        try:
            for root, dirs, files in os.walk(cls.img_tmp_directory, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(cls.img_tmp_directory)
        except OSError as e:
            print("Error: %s : %s" % (cls.img_tmp_directory, e.strerror))

    @classmethod
    def save_image_to_tmp_folder(cls, image_data, id):
        img = Image.open(image_data)
        img.save(cls.img_tmp_directory +"/" + str(id) + ".jpg")
