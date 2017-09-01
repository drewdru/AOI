import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image


def readImage(path):
    # Read in the image
    image = mpimg.imread(path)

    # Grab the x and y size and make a copy of the image
    ysize = image.shape[0]
    xsize = image.shape[1]
    return image


def copyImage(image):
    color_select = np.copy(image)
    return color_select


def displayAndSaveImage(img, path):
    img2 = Image.fromarray(np.asarray(np.clip(img, 0, 255), dtype="uint8"))
    img2.show()
    print(path)
    img2.save(path)
    plt.imshow(img)
    #mpimg.imsave(path, img)

def saveImageWithCmap(img, path, cmap):
    img2 = Image.fromarray(np.asarray(np.clip(img, 0, 255), dtype="uint8"))
    img2.show()
    print(path)
    img2.save(path)
    #mpimg.imsave(path, img, cmap=cmap)
