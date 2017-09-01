import glob 
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel
from imageSegmentation import segmentation
from imageMorphology import edgeDetection
from imageFilters import filters

#---------------------------------------------------------
#thresholding functions

def abs_canny_thresh(image, thresh=(0.7, 5)):
    gray = colorModel.rgbToYuv(image, gray.shape)
    gray = colorModel.yuvToGrayscaleRgb(gray, gray.shape)
    gaussianImg = img.copy()
    gaussianDeviation = 1.0 ##############################################
    gaussianFilterSize = math.floor(gaussianDeviation*3.0)
    filters.gaussianBlur('RGB', 0, gaussianImg.load(),
                gaussianImg.size, (gaussianFilterSize, gaussianFilterSize))
    edgeDetection.canny('RGB', 0, img.load(), img.size,
        gaussianImg.load(), 1, thresh)

    scaled_canny = np.uint8(255*gray/np.max(gray))

    canny_thresh = np.zeros_like(scaled_canny)
    canny_thresh[(scaled_canny > thresh[0]) & (scaled_canny < thresh[1])] = 1

    return canny_thresh


def mag_thresh(image, thresh=(1, 5)):
    gray = colorModel.rgbToYuv(image, gray.shape)
    gray = colorModel.yuvToGrayscaleRgb(gray, gray.shape)
    gaussianImg = img.copy()
    gaussianDeviation = 1.0 ##############################################
    gaussianFilterSize = math.floor(gaussianDeviation*3.0)
    filters.gaussianBlur('RGB', 0, gaussianImg.load(),
                gaussianImg.size, (gaussianFilterSize, gaussianFilterSize))
    edgeDetection.canny('RGB', 0, img.load(), img.size,
        gaussianImg.load(), 1, thresh)

    scaled_magnitude = np.uint8(255*gray_magnitude/np.max(gray_magnitude))

    mag_thresh = np.zeros_like(scaled_magnitude)
    mag_thresh[(scaled_magnitude > thresh[0]) & (scaled_magnitude < thresh[1])] = 1

    return mag_thresh

def dir_thresh(image, thresh=(0, np.pi/2)):
    gray = colorModel.rgbToYuv(image, gray.shape)
    gray = colorModel.yuvToGrayscaleRgb(gray, gray.shape)
    gaussianImg = img.copy()
    gaussianDeviation = 1.0 ##############################################
    gaussianFilterSize = math.floor(gaussianDeviation*3.0)
    filters.gaussianBlur('RGB', 0, gaussianImg.load(),
                gaussianImg.size, (gaussianFilterSize, gaussianFilterSize))
    edgeDetection.canny('RGB', 0, img.load(), img.size,
        gaussianImg.load(), 1, thresh)

    dir_threshold = np.zeros_like(gray)
    dir_threshold[(gray > thresh[0]) & (gray < thresh[1])] = 1

    return dir_threshold

def rgb_thresh(image, channel="r", thresh=(0, 1)):
    if channel=="r":
        threshold_channel = image[:,:,0] * 255
    if channel=="g":
        threshold_channel = image[:,:,1] * 255
    if channel=="b":
        threshold_channel = image[:,:,2] * 255

    rgb_threshold = np.zeros_like(threshold_channel)
    rgb_threshold[(threshold_channel > thresh[0]) & (threshold_channel < thresh[1])] = 1
    return rgb_threshold

def hls_thresh(image, channel="h", thresh=(0, 50)):
    hls = colorModel.rgbToHsl(image)

    if channel=="h":
        threshold_channel = hls[:,:,0] * 255
    if channel=="l":
        threshold_channel = hls[:,:,1] * 255
    if channel=="s":
        threshold_channel = hls[:,:,2] * 255

    hls_threshold = np.zeros_like(threshold_channel)
    hls_threshold[(threshold_channel > thresh[0]) & (threshold_channel < thresh[1])] = 1
    return hls_threshold

def filterf(image):
    height, width = image.shape[0], image.shape[1]
    bl = (width / 2 - 480, height - 30)
    br = (width / 2 + 480, height - 30)
    tl = (width / 2 - 60, height / 2 + 60)
    tr = (width / 2 + 60, height / 2 + 60)

    fit_left = np.polyfit((bl[0], tl[0]), (bl[1], tl[1]), 1)
    fit_right = np.polyfit((br[0], tr[0]), (br[1], tr[1]), 1)
    fit_bottom = np.polyfit((bl[0], br[0]), (bl[1], br[1]), 1)
    fit_top = np.polyfit((tl[0], tr[0]), (tl[1], tr[1]), 1)

    # Find the region inside the lines
    xs, ys = np.meshgrid(np.arange(0, image.shape[1]), np.arange(0, image.shape[0]))
    mask = (ys > (xs * fit_left[0] + fit_left[1])) & \
           (ys > (xs * fit_right[0] + fit_right[1])) & \
           (ys > (xs * fit_top[0] + fit_top[1])) & \
           (ys < (xs * fit_bottom[0] + fit_bottom[1]))

    img_window = image
    img_window[mask == False] = 0
    return img_window



#---------------------------------------------------------------
#exploratory research
def exploratory():
    #read image
    image = plt.imread('./test_images/undistorted7.jpg')

    #processing functions
    abs_sobel_thresh_1 = abs_sobel_thresh(image,thresh= (20,100))
    mag_thresh_1 = mag_thresh(image, thresh= (60,100))
    dir_thresh_1 = dir_thresh(image, thresh= (-np.pi/4,np.pi/4))
    rgb_thresh_1 = rgb_thresh(image, channel="r", thresh=(0,100))
    hls_thresh_1 = hls_thresh(image, channel="s", thresh=(0,110))
    

    #combined threshold function
    combined = np.zeros_like(image[:,:,0])
    combined[hls_thresh_1 == 1] = 1
    combined[abs_sobel_thresh_1 == 1] = 1

    #window
    windowed = filterf(combined)


    #plotting
    f, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(1,8, figsize=(20,10))
    ax1.imshow(image)
    ax1.set_title('Original', fontsize=10)

    ax2.imshow(abs_sobel_thresh_1, cmap='gray')
    ax2.set_title('Abs. Sobel Thresh.', fontsize=10)

    ax3.imshow(mag_thresh_1, cmap='gray')
    ax3.set_title('Mag. Sobel Thresh.', fontsize=10)

    ax4.imshow(dir_thresh_1, cmap='gray')
    ax4.set_title('Dir. Sobel Thresh.', fontsize=10)

    ax5.imshow(rgb_thresh_1, cmap='gray')
    ax5.set_title('RGB Thresh.', fontsize=10)

    ax6.imshow(hls_thresh_1, cmap='gray')
    ax6.set_title('HLS Thresh.', fontsize=10)

    ax7.imshow(combined, cmap='gray')
    ax7.set_title('Combined Tresh.', fontsize=10)

    ax8.imshow(windowed, cmap='gray')
    ax8.set_title('Windowed', fontsize=10)


    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    plt.show()

#exploratory()


#preprocess images
#--------------------------------------------------------

def preprocess():

    undistorted = glob.glob('./test_images/undistorted*.jpg')

    for idx, name in enumerate(undistorted):
        #read image
        undist = plt.imread(name)

        #processing functions
        abs_sobel_thresh_1 = abs_sobel_thresh(undist, orient='x', sobel_kernel = 25, thresh= (30,100))
        mag_thresh_1 = mag_thresh(undist, sobel_kernel = 3,thresh= (60,100))
        dir_thresh_1 = dir_thresh(undist, sobel_kernel = 9, thresh= (-np.pi/4,np.pi/4))
        rgb_thresh_1 = rgb_thresh(undist, channel="r", thresh=(0,100))
        hls_thresh_1 = hls_thresh(undist, channel="s", thresh=(0,110))
        

        #combined threshold function
        combined = np.zeros_like(undist[:,:,0])
        combined[hls_thresh_1 == 1] = 1
        combined[mag_thresh_1 == 1] = 1

        #window
        windowed = window(combined)

        write_name = './test_images/preprocessed'+str(idx)+'.jpg'
        plt.imsave(write_name, windowed, cmap = 'gray')

#preprocess()





#transform images
#--------------------------------------------------------

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

def transform():
    preprocessed = glob.glob('./test_images/preprocessed*.jpg')

    for idx, name in enumerate(preprocessed):
        #read image
        img = plt.imread(name)
        img_size = (img.shape[1], img.shape[0])

        #trapazoid source points to rectangular destination points 
        src = np.float32([(257, 685), (1050, 685), (583, 460),(702, 460)])
        dst = np.float32([(200, 720), (1080, 720), (200, 0), (1080, 0)])

        #perspective tranform matrix
        M = find_coeffs(src, dst)

        #transform
        transformed = find_coeffs(img, M)

        #write
        write_name = './test_images/transformed'+str(idx)+'.jpg'
        cv2.imwrite(write_name, transformed)

#transform()











































































from .camera_cal.gen import *

