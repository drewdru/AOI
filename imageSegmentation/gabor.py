import skimage.filters as filters
#for i in dir(module): print i
from skimage import data, io
#from matplotlib import pyplot as plt  
from skimage.util import img_as_float
from skimage.exposure import equalize_hist
from PIL import Image
import numpy as np
np.set_printoptions(threshold=np.nan)
import time
from skimage.color import rgb2gray

def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.asarray( img, dtype="uint8" )
    floatData = img_as_float(data)
    return floatData


def show_images(images,titles=None):
    """Display a list of images"""
    n_ims = len(images)
    if titles is None: titles = ['(%d)' % i for i in range(1,n_ims + 1)]
    fig = plt.figure()
    n = 1
    for image,title in zip(images,titles):
        a = fig.add_subplot(1,n_ims,n) # Make subplot
        #if image.ndim == 2: # Is image grayscale?
        #    plt.gray() # Only place in this blog you can't replace 'gray' with 'grey'
        plt.imshow(image)
        a.set_title(title)
        n += 1
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_ims)
    plt.show()


def doGabor(imgPath, outImagePath):
    image = io.imread(imgPath)
    #grayImg = rgb2gray(image)
    im = image[:,:,0]
    im = np.interp(im, [0, 255],[0,1])


    #thetas = [0,np.pi/4, np.pi/2, np.pi/8, np.pi, np.pi+(np.pi/8),np.pi+(np.pi/4),np.pi+(np.pi/2)]
    #thetas = [0, np.pi/2, np.pi, np.pi*2]
    #thetas = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,-0.1,-0.2,-0.3,-0.4,-0.5,-0.6,-0.7,-0.8,-0.9]
    thetas = [0.0,np.pi/2]

    summedVals = np.zeros(im.shape)

    for i in range(len(thetas)):
        filt_real, filt_img = filters.gabor_filter(im, frequency=1.9, theta = thetas[i],bandwidth=0.5, n_stds=3)
        summedVals += filt_img
        print (i)

    #summedVals = equalize_hist(summedVals)
    summedVals = np.absolute(summedVals)
    #summedVals *= im
    maxVal = np.amax(summedVals)
    minVal = np.amin(summedVals)
    mapped = np.interp(summedVals, [minVal, maxVal],[0,255])
    out = np.uint8(mapped)
    bb = Image.fromarray(out)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    bb.save(outImagePath)
    # bb.show()

    #doGabor(summedVals)


