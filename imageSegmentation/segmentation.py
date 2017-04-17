"""
    @package segmentation
    Image segmentation 
"""
import scipy.ndimage as ndi
import scipy
import math
import sys
import os
import numpy

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageFilters import apertureService
from imageProcessor import colorModel
from PyQt5.QtCore import QCoreApplication
from PIL import Image, ImageChops


def roberts(colorModelTag, currentImageChannelIndex, pixels, imgSize,
        tempPixels, amplifier=1.0, threshold=10):
    for y in range(imgSize[0]):
        QCoreApplication.processEvents()
        for x in range(imgSize[1]):
            accXValueSumR = 0.0
            accYValueSumR = 0.0
            accXValueSumG = 0.0
            accYValueSumG = 0.0
            accXValueSumB = 0.0
            accYValueSumB = 0.0

            rightX = x+1
            bottomY = y+1

            hasBottom = bottomY < imgSize[0]
            hasRight = rightX < imgSize[1]

            if hasBottom:
                if hasRight:
                    # X accumulator
                    factor = -1.0
                    # accXValueSum += bwImg[bottomY*width+rightX]*factor;
                    r, g, b = tempPixels[bottomY, rightX]
                    accXValueSumR += r * factor
                    accXValueSumG += g * factor
                    accXValueSumB += b * factor
                else:
                    # Extend the image by 1 pixel on each side and using the outmost pixels in order to
                    # avoid false positives on the borders of the image

                    # X accumulator
                    factor = -1.0
                    # accXValueSum += bwImg[bottomY*width+x]*factor
                    r, g, b = tempPixels[bottomY, x]
                    accXValueSumR += r * factor
                    accXValueSumG += g * factor
                    accXValueSumB += b * factor
                # Y accumulator
                factor = -1.0
                # accYValueSum += bwImg[bottomY*width+x]*factor
                r, g, b = tempPixels[bottomY, x]
                accYValueSumR += r * factor
                accYValueSumG += g * factor
                accYValueSumB += b * factor
            else:
                if hasRight:
                    #  X accumulator
                    factor = -1.0
                    # accXValueSum += bwImg[y*width+rightX]*factor
                    r, g, b = tempPixels[y, rightX]
                    accXValueSumR += r * factor
                    accXValueSumG += g * factor
                    accXValueSumB += b * factor
                else:
                    # X accumulator
                    factor = -1.0
                    # accXValueSum += bwImg[y*width+x]*factor
                    r, g, b = tempPixels[y, x]
                    accXValueSumR += r * factor
                    accXValueSumG += g * factor
                    accXValueSumB += b * factor
                # Y accumulator
                factor = -1.0
                # accYValueSum += bwImg[y*width+x]*factor
                r, g, b = tempPixels[y, x]
                accYValueSumR += r * factor
                accYValueSumG += g * factor
                accYValueSumB += b * factor
            if hasRight:
                # Y accumulator
                factor = 1.0
                # accYValueSum += bwImg[y*width+rightX]*factor
                r, g, b = tempPixels[y, rightX]
                accYValueSumR += r * factor
                accYValueSumG += g * factor
                accYValueSumB += b * factor
            else:
                # Y accumulator
                factor = 1.0
                # accYValueSum += bwImg[y*width+x]*factor
                r, g, b = tempPixels[y, x]
                accYValueSumR += r * factor
                accYValueSumG += g * factor
                accYValueSumB += b * factor
            # This pixel:
            # X accumulator
            factor = 1.0
            # accXValueSum += bwImg[y*width+x]*factor
            r, g, b = tempPixels[y, x]
            accXValueSumR += r * factor
            accXValueSumG += g * factor
            accXValueSumB += b * factor

            resultR = amplifier*math.sqrt(math.pow(accXValueSumR,2.0)+math.pow(accYValueSumR,2.0))
            resultG = amplifier*math.sqrt(math.pow(accXValueSumG,2.0)+math.pow(accYValueSumG,2.0))
            resultB = amplifier*math.sqrt(math.pow(accXValueSumB,2.0)+math.pow(accYValueSumB,2.0))

            if resultR < threshold: resultR = 0
            if resultG < threshold: resultG = 0
            if resultB < threshold: resultB = 0
            oldR, oldG, oldB = pixels[y, x]
            if currentImageChannelIndex == 0:
                pixels[y, x] = (
                    int(resultR), int(resultG), int(resultB))
            if currentImageChannelIndex == 1:
                pixels[y, x] = (
                    int(resultR), oldG, oldB)
            if currentImageChannelIndex == 2:
                pixels[y, x] = (
                    oldR, int(resultG), oldB)
            if currentImageChannelIndex == 3:
                pixels[y, x] = (
                    oldR, oldG, int(resultB))



def canny(colorModelTag, currentImageChannelIndex, pixels, imgSize,
        G, amplifier=1.0, threshold=(10, 250)):
    sigma = 2.2
    
    gradxR = []
    gradyR = []
    gradxG = []
    gradyG = []
    gradxB = []
    gradyB = []

    sobel_x = [[-1,0,1],
            [-2,0,2],
            [-1,0,1]]
    sobel_y = [[-1,-2,-1],
            [0,0,0],
            [1,2,1]]

    width = imgSize[1]
    height = imgSize[0]

    #calculate |G| and dir(G)
    for x in range(1, width-1):
        gradxLineR = []
        gradyLineR = []
        gradxLineG = []
        gradyLineG = []
        gradxLineB = []
        gradyLineB = []
        for y in range(1, height-1):
            # print(sobel_x[0][0])
            # print(G[x-1,y-1][0])
            pxR = (sobel_x[0][0] * G[x-1,y-1][0]) + (sobel_x[0][1] * G[x,y-1][0]) + \
                (sobel_x[0][2] * G[x+1,y-1][0]) + (sobel_x[1][0] * G[x-1,y][0]) + \
                (sobel_x[1][1] * G[x,y][0]) + (sobel_x[1][2] * G[x+1,y][0]) + \
                (sobel_x[2][0] * G[x-1,y+1][0]) + (sobel_x[2][1] * G[x,y+1][0]) + \
                (sobel_x[2][2] * G[x+1,y+1][0])

            pyR = (sobel_y[0][0] * G[x-1,y-1][0]) + (sobel_y[0][1] * G[x,y-1][0]) + \
                (sobel_y[0][2] * G[x+1,y-1][0]) + (sobel_y[1][0] * G[x-1,y][0]) + \
                (sobel_y[1][1] * G[x,y][0]) + (sobel_y[1][2] * G[x+1,y][0]) + \
                (sobel_y[2][0] * G[x-1,y+1][0]) + (sobel_y[2][1] * G[x,y+1][0]) + \
                (sobel_y[2][2] * G[x+1,y+1][0])

            pxG = (sobel_x[0][0] * G[x-1,y-1][1]) + (sobel_x[0][1] * G[x,y-1][1]) + \
                (sobel_x[0][2] * G[x+1,y-1][1]) + (sobel_x[1][0] * G[x-1,y][1]) + \
                (sobel_x[1][1] * G[x,y][1]) + (sobel_x[1][2] * G[x+1,y][1]) + \
                (sobel_x[2][0] * G[x-1,y+1][1]) + (sobel_x[2][1] * G[x,y+1][1]) + \
                (sobel_x[2][2] * G[x+1,y+1][1])

            pyG = (sobel_y[0][0] * G[x-1,y-1][1]) + (sobel_y[0][1] * G[x,y-1][1]) + \
                (sobel_y[0][2] * G[x+1,y-1][1]) + (sobel_y[1][0] * G[x-1,y][1]) + \
                (sobel_y[1][1] * G[x,y][1]) + (sobel_y[1][2] * G[x+1,y][1]) + \
                (sobel_y[2][0] * G[x-1,y+1][1]) + (sobel_y[2][1] * G[x,y+1][1]) + \
                (sobel_y[2][2] * G[x+1,y+1][1])

            pxB = (sobel_x[0][0] * G[x-1,y-1][0]) + (sobel_x[0][1] * G[x,y-1][0]) + \
                (sobel_x[0][2] * G[x+1,y-1][0]) + (sobel_x[1][0] * G[x-1,y][0]) + \
                (sobel_x[1][1] * G[x,y][0]) + (sobel_x[1][2] * G[x+1,y][0]) + \
                (sobel_x[2][0] * G[x-1,y+1][0]) + (sobel_x[2][1] * G[x,y+1][0]) + \
                (sobel_x[2][2] * G[x+1,y+1][0])

            pyB = (sobel_y[0][0] * G[x-1,y-1][2]) + (sobel_y[0][1] * G[x,y-1][2]) + \
                (sobel_y[0][2] * G[x+1,y-1][2]) + (sobel_y[1][0] * G[x-1,y][2]) + \
                (sobel_y[1][1] * G[x,y][2]) + (sobel_y[1][2] * G[x+1,y][2]) + \
                (sobel_y[2][0] * G[x-1,y+1][2]) + (sobel_y[2][1] * G[x,y+1][2]) + \
                (sobel_y[2][2] * G[x+1,y+1][2])
            gradxLineR.append(pxR)
            gradyLineR.append(pyR)
            gradxLineG.append(pxG)
            gradyLineG.append(pyG)
            gradxLineB.append(pxB)
            gradyLineB.append(pyB)
        gradxR.append(gradxLineR)
        gradyR.append(gradyLineR)
        gradxG.append(gradxLineG)
        gradyG.append(gradyLineG)
        gradxB.append(gradxLineB)
        gradyB.append(gradyLineB)

    sobeloutmagR = scipy.hypot(gradxR, gradyR)
    sobeloutdirR = scipy.arctan2(gradyR, gradxR)
    sobeloutmagG = scipy.hypot(gradxG, gradyG)
    sobeloutdirG = scipy.arctan2(gradyG, gradxG)
    sobeloutmagB = scipy.hypot(gradxB, gradyB)
    sobeloutdirB = scipy.arctan2(gradyB, gradxB)

    # scipy.misc.imsave('cannynewmag.jpg', sobeloutmagR)
    # scipy.misc.imsave('cannynewdir.jpg', sobeloutdirR)

    # scipy.misc.imsave('cannynewmag.jpg', sobeloutmagG)
    # scipy.misc.imsave('cannynewdir.jpg', sobeloutdirG)

    # scipy.misc.imsave('cannynewmag.jpg', sobeloutmagB)
    # scipy.misc.imsave('cannynewdir.jpg', sobeloutdirB)

    for x in range(width-2):
        for y in range(height-2):
            if (sobeloutdirR[x][y]<22.5 and sobeloutdirR[x][y]>=0) or \
                    (sobeloutdirR[x][y]>=157.5 and sobeloutdirR[x][y]<202.5) or \
                    (sobeloutdirR[x][y]>=337.5 and sobeloutdirR[x][y]<=360):
                sobeloutdirR[x][y]=0
            elif (sobeloutdirR[x][y]>=22.5 and sobeloutdirR[x][y]<67.5) or \
                    (sobeloutdirR[x][y]>=202.5 and sobeloutdirR[x][y]<247.5):
                sobeloutdirR[x][y]=45
            elif (sobeloutdirR[x][y]>=67.5 and sobeloutdirR[x][y]<112.5)or \
                    (sobeloutdirR[x][y]>=247.5 and sobeloutdirR[x][y]<292.5):
                sobeloutdirR[x][y]=90
            else:
                sobeloutdirR[x][y]=135
            
            if (sobeloutdirG[x][y]<22.5 and sobeloutdirG[x][y]>=0) or \
                    (sobeloutdirG[x][y]>=157.5 and sobeloutdirG[x][y]<202.5) or \
                    (sobeloutdirG[x][y]>=337.5 and sobeloutdirG[x][y]<=360):
                sobeloutdirG[x][y]=0
            elif (sobeloutdirG[x][y]>=22.5 and sobeloutdirG[x][y]<67.5) or \
                    (sobeloutdirG[x][y]>=202.5 and sobeloutdirG[x][y]<247.5):
                sobeloutdirG[x][y]=45
            elif (sobeloutdirG[x][y]>=67.5 and sobeloutdirG[x][y]<112.5)or \
                    (sobeloutdirG[x][y]>=247.5 and sobeloutdirG[x][y]<292.5):
                sobeloutdirG[x][y]=90
            else:
                sobeloutdirG[x][y]=135
            
            if (sobeloutdirB[x][y]<22.5 and sobeloutdirB[x][y]>=0) or \
                    (sobeloutdirB[x][y]>=157.5 and sobeloutdirB[x][y]<202.5) or \
                    (sobeloutdirB[x][y]>=337.5 and sobeloutdirB[x][y]<=360):
                sobeloutdirB[x][y]=0
            elif (sobeloutdirB[x][y]>=22.5 and sobeloutdirB[x][y]<67.5) or \
                    (sobeloutdirB[x][y]>=202.5 and sobeloutdirB[x][y]<247.5):
                sobeloutdirB[x][y]=45
            elif (sobeloutdirB[x][y]>=67.5 and sobeloutdirB[x][y]<112.5)or \
                    (sobeloutdirB[x][y]>=247.5 and sobeloutdirB[x][y]<292.5):
                sobeloutdirB[x][y]=90
            else:
                sobeloutdirB[x][y]=135


    # scipy.misc.imsave('cannynewdirquantize.jpg', sobeloutdirR)
    # scipy.misc.imsave('cannynewdirquantize.jpg', sobeloutdirG)
    # scipy.misc.imsave('cannynewdirquantize.jpg', sobeloutdirB)

    mag_supR = sobeloutmagR.copy()
    mag_supG = sobeloutmagG.copy()
    mag_supB = sobeloutmagB.copy()

    for x in range(1, width-3):
        for y in range(1, height-3):
            if sobeloutdirR[x][y]==0:
                if (sobeloutmagR[x][y]<=sobeloutmagR[x][y+1]) or \
                (sobeloutmagR[x][y]<=sobeloutmagR[x][y-1]):
                    mag_supR[x][y]=0
            elif sobeloutdirR[x][y]==45:
                if (sobeloutmagR[x][y]<=sobeloutmagR[x-1][y+1]) or \
                (sobeloutmagR[x][y]<=sobeloutmagR[x+1][y-1]):
                    mag_supR[x][y]=0
            elif sobeloutdirR[x][y]==90:
                if (sobeloutmagR[x][y]<=sobeloutmagR[x+1][y]) or \
                (sobeloutmagR[x][y]<=sobeloutmagR[x-1][y]):
                    mag_supR[x][y]=0
            else:
                if (sobeloutmagR[x][y]<=sobeloutmagR[x+1][y+1]) or \
                (sobeloutmagR[x][y]<=sobeloutmagR[x-1][y-1]):
                    mag_supR[x][y]=0

            if sobeloutdirG[x][y]==0:
                if (sobeloutmagG[x][y]<=sobeloutmagG[x][y+1]) or \
                (sobeloutmagG[x][y]<=sobeloutmagG[x][y-1]):
                    mag_supG[x][y]=0
            elif sobeloutdirG[x][y]==45:
                if (sobeloutmagG[x][y]<=sobeloutmagG[x-1][y+1]) or \
                (sobeloutmagG[x][y]<=sobeloutmagG[x+1][y-1]):
                    mag_supG[x][y]=0
            elif sobeloutdirG[x][y]==90:
                if (sobeloutmagG[x][y]<=sobeloutmagG[x+1][y]) or \
                (sobeloutmagG[x][y]<=sobeloutmagG[x-1][y]):
                    mag_supG[x][y]=0
            else:
                if (sobeloutmagG[x][y]<=sobeloutmagG[x+1][y+1]) or \
                (sobeloutmagG[x][y]<=sobeloutmagG[x-1][y-1]):
                    mag_supG[x][y]=0

            if sobeloutdirB[x][y]==0:
                if (sobeloutmagB[x][y]<=sobeloutmagB[x][y+1]) or \
                (sobeloutmagB[x][y]<=sobeloutmagB[x][y-1]):
                    mag_supB[x][y]=0
            elif sobeloutdirB[x][y]==45:
                if (sobeloutmagB[x][y]<=sobeloutmagB[x-1][y+1]) or \
                (sobeloutmagB[x][y]<=sobeloutmagB[x+1][y-1]):
                    mag_supB[x][y]=0
            elif sobeloutdirB[x][y]==90:
                if (sobeloutmagB[x][y]<=sobeloutmagB[x+1][y]) or \
                (sobeloutmagB[x][y]<=sobeloutmagB[x-1][y]):
                    mag_supB[x][y]=0
            else:
                if (sobeloutmagB[x][y]<=sobeloutmagB[x+1][y+1]) or \
                (sobeloutmagB[x][y]<=sobeloutmagB[x-1][y-1]):
                    mag_supB[x][y]=0

    # scipy.misc.imsave('cannynewmagsup.jpg', mag_supR)
    # scipy.misc.imsave('cannynewmagsup.jpg', mag_supG)
    # scipy.misc.imsave('cannynewmagsup.jpg', mag_supB)

    mR = numpy.max(mag_supR)
    mG = numpy.max(mag_supG)
    mB = numpy.max(mag_supB)
    thR = 0.2*mR
    tlR = 0.1*mR
    thG = 0.2*mG
    tlG = 0.1*mG
    thB = 0.2*mB
    tlB = 0.1*mB


    gnhR = numpy.zeros((width, height))
    gnlR = numpy.zeros((width, height))
    gnhG = numpy.zeros((width, height))
    gnlG = numpy.zeros((width, height))
    gnhB = numpy.zeros((width, height))
    gnlB = numpy.zeros((width, height))

    for x in range(width-2):
        for y in range(height-2):
            if mag_supR[x][y]>=thR:
                gnhR[x][y]=mag_supR[x][y]
            if mag_supR[x][y]>=tlR:
                gnlR[x][y]=mag_supR[x][y]
            if mag_supG[x][y]>=thG:
                gnhR[x][y]=mag_supG[x][y]
            if mag_supG[x][y]>=tlG:
                gnlG[x][y]=mag_supG[x][y]
            if mag_supB[x][y]>=thB:
                gnhB[x][y]=mag_supB[x][y]
            if mag_supB[x][y]>=tlB:
                gnlB[x][y]=mag_supB[x][y]
    # scipy.misc.imsave('cannynewgnlbeforeminus.jpg', gnlR)
    # scipy.misc.imsave('cannynewgnlbeforeminus.jpg', gnlG)
    # scipy.misc.imsave('cannynewgnlbeforeminus.jpg', gnlB)
    gnlR = gnlR-gnhR
    gnlG = gnlG-gnhG
    gnlB = gnlB-gnhB
    # scipy.misc.imsave('cannynewgnlafterminus.jpg', gnlR)
    # scipy.misc.imsave('cannynewgnlafterminus.jpg', gnlG)
    # scipy.misc.imsave('cannynewgnlafterminus.jpg', gnlB)
    # scipy.misc.imsave('cannynewgnh.jpg', gnhR)
    # scipy.misc.imsave('cannynewgnh.jpg', gnhG)
    # scipy.misc.imsave('cannynewgnh.jpg', gnhB)


    def traverse(i, j):
        x = [-1, 0, 1, -1, 1, -1, 0, 1]
        y = [-1, -1, -1, 0, 0, 1, 1, 1]
        for k in range(8):
            if gnhR[i+x[k]][j+y[k]]==0 and gnlR[i+x[k]][j+y[k]]!=0:
                gnhR[i+x[k]][j+y[k]]=255
                traverse(i+x[k], j+y[k])
            if gnhG[i+x[k]][j+y[k]]==0 and gnlG[i+x[k]][j+y[k]]!=0:
                gnhG[i+x[k]][j+y[k]]=255
                traverse(i+x[k], j+y[k])
            if gnhB[i+x[k]][j+y[k]]==0 and gnlB[i+x[k]][j+y[k]]!=0:
                gnhB[i+x[k]][j+y[k]]=255
                traverse(i+x[k], j+y[k])

    for i in range(1, width-1):
        for j in range(1, height-1):
            if gnhR[i][j]:
                gnhR[i][j]=255
                traverse(i, j)
            if gnhG[i][j]:
                gnhG[i][j]=255
                traverse(i, j)
            if gnhB[i][j]:
                gnhB[i][j]=255
                traverse(i, j)
    
    for y in range(imgSize[0]):
        QCoreApplication.processEvents()
        for x in range(imgSize[1]):
            print((int(gnhR[y][x]), int(gnhG[y][x]), int(gnhB[y][x])))
            oldR, oldG, oldB = pixels[y, x]
            if currentImageChannelIndex == 0:
                pixels[y, x] = (
                    int(gnhR[y][x]), int(gnhG[y][x]), int(gnhB[y][x]))
            if currentImageChannelIndex == 1:
                pixels[y, x] = (
                    int(gnhR[y][x]), oldG, oldB)
            if currentImageChannelIndex == 2:
                pixels[y, x] = (
                    oldR, int(gnhG[y][x]), oldB)
            if currentImageChannelIndex == 3:
                pixels[y, x] = (
                    oldR, oldG, int(gnhB[y][x]))
    # scipy.misc.imsave('cannynewout.jpg', gnhR)
    # scipy.misc.imsave('cannynewout.jpg', gnhG)
    # scipy.misc.imsave('cannynewout.jpg', gnhB)
