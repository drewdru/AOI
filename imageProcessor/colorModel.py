"""
    @package colorModel
    Change color model
"""

from PIL import Image
import threading
import multiprocessing
import math
import numpy
from PyQt5.QtCore import QCoreApplication

def viewYUVChannelByID(pixels, size, channelID):
    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            channelsList = []
            for indx, channel in enumerate(pixels[i, j]):
                if indx == channelID:
                    channelsList.append(channel)
                else:
                    channelsList.append(128)
            pixels[i, j] = tuple(channelsList)

def viewRGBChannelByID(pixels, size, channelID):
    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            channelsList = []
            for indx, channel in enumerate(pixels[i, j]):
                if indx == channelID:
                    channelsList.append(channel)
                else:
                    channelsList.append(0)
            pixels[i, j] = tuple(channelsList)

def changeRgbBalance(pixels, size, rValue, gValue, bValue):
    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                int(r + rValue),
                int(g + gValue),
                int(b + bValue)
            )

def rgbToYuv(pixels, size, yValue=0, uValue=0, vValue=0):
    """
        Change color model from RGB to YUV

        @param pixels The pixels from Pillow RGB Image
        @param size The width and height
    """
    # Y = 0.299 * R + 0.587 * G + 0.114 * B;
    # U = -0.14713 * R - 0.28886 * G + 0.436 * B + 128;
    # V = 0.615 * R - 0.51499 * G - 0.10001 * B + 128;
    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            r, g, b = pixels[i, j]
            Y = 0.299*r + 0.587*g + 0.114*b
            U = -0.14713*r - 0.28886*g + 0.436*b + 128
            V = 0.615*r - 0.51499*g - 0.10001*b + 128

            if Y >= 0 and Y <= 255: pass
            elif Y < 0: Y = 0
            else: Y = 255

            if U >= 0 and U <= 255: pass
            elif U < 0: U = 0
            else: U = 255

            if V >= 0 and V <= 255: pass
            elif V < 0: V = 0
            else: V = 255

            Y = Y + yValue
            if uValue != 0:
                U = (U + uValue)/2
            if vValue != 0:
                V = (V + vValue)/2

            pixels[i, j] = (int(Y), int(U), int(V))

def yuvToRgb(pixels, size):
    """
        Change color model from YUV to RGB

        @param pixels The pixels from Pillow YUV Image
        @param size The width and height
    """
    # R = Y + 1.13983 * (V - 128);
    # G = Y - 0.39465 * (U - 128) - 0.58060 * (V - 128);
    # B = Y + 2.03211 * (U - 128);
    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            y, u, v = pixels[i, j]
            R = y + 1.13983*(v - 128)
            G = y - 0.39465*(u - 128) - 0.58060*(v - 128)
            B = y + 2.03211*(u - 128)

            if R >= 0 and R <= 255: y = R
            elif R < 0: y = 0
            else: y = 255

            if G >= 0 and G <= 255: u = G
            elif G < 0: u = 0
            else: u = 255

            if B >= 0 and B <= 255: v = B
            elif B < 0: v = 0
            else: v = 255

            pixels[i, j] = (int(y), int(u), int(v))

def yuvToGrayscaleRgb(pixels, size):
    """
        Change color from YUV to grayscale RGB

        @param pixels The pixels from Pillow YUV Image
        @param size The width and height
    """
    # R = Y + 1.13983 * (V - 128);
    # G = Y - 0.39465 * (U - 128) - 0.58060 * (V - 128);
    # B = Y + 2.03211 * (U - 128);
    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            y, u, v = pixels[i, j]

            R = y
            G = y
            B = y

            if R >= 0 and R <= 255: y = R
            elif R < 0: y = 0
            else: y = 255

            if G >= 0 and G <= 255: u = G
            elif G < 0: u = 0
            else: u = 255

            if B >= 0 and B <= 255: v = B
            elif B < 0: v = 0
            else: v = 255

            pixels[i, j] = (int(y), int(u), int(v))


def rgbToHsl(pixelsArray, value=None, hValue=0, sValue=0, lValue=0):
    """
        Change color model from RGB to HSL

        @param pixelsArray The numpy array is a Pillow RGB Image
    """
    print("pixelsArray, value, hValue, sValue, sValue")
    print(pixelsArray, value, hValue, sValue, sValue)
    for i, pixels in enumerate(pixelsArray):
        QCoreApplication.processEvents()
        for j, pixel in enumerate(pixels):
            r, g, b = pixelsArray[i, j]
            pixelsArray[i, j] = colorRgbToHsl(r, g, b, value, hValue, sValue, lValue) # (H, S, L)
    return pixelsArray

def colorRgbToHsl(r, g, b, value=None, hValue=0, sValue=0, lValue=0):
    r /= 255
    g /= 255
    b /= 255
    mx = max(r, g, b)
    mn = min(r, g, b)
    l = (mx + mn)/2
    if mx == mn:
        h = s = 0
    else:
        d = mx - mn
        if l > 0.5:
            s = d/(2 - mx - mn)
        else:
            s = d/(mx + mn)
        if mx == r:
            c = 0
            if g < b:
                c = 6
            h = (g - b)/d + c
        elif mx == g:
            h = (b - r)/d + 2
        elif mx == b:
            h = (r - g)/d + 4
        h /= 6

    if not value is None: h = value
    elif hValue != 0: h = abs(hValue)
    else: h = h*100
    s = s*100 + sValue
    l = l*100 + lValue
    if s < 0: s = 0
    if s > 100: s = 100
    if l < 0: l = 0
    if l > 100: l = 100
    return (_rod2(h), _rod2(s), _rod2(l))

def hslToRgb(pixelsArray):
    """
        Change color model from HSL to RGB

        @param pixelsArray The numpy array is a Pillow RGB Image
    """
    for i, pixels in enumerate(pixelsArray):
        QCoreApplication.processEvents()
        for j, pixel in enumerate(pixels):
            h, s, l = pixelsArray[i, j]
            pixelsArray[i, j] = colorHslToRgb(h, s, l)
    return pixelsArray


def colorHslToRgb(h, s, l):
    h /= 360
    s /= 100
    l /= 100
    if s == 0:
        r = g = b = l
    else:
        if l < 0.5:
            q = l*(1 + s)
        else:
            q = l + s - l*s
        p = 2 * l - q
        r = _hue2rgb(p, q, h + 1 / 3)
        g = _hue2rgb(p, q, h)
        b = _hue2rgb(p, q, h - 1 / 3)
    return (_rod(r*255), _rod(g*255), _rod(b*255))

def _rod(no):
    return int(no//1 + ((no%1)/0.5)//1)

def _rod2(no):
    return round(no, 2)

def _hue2rgb(p, q, t):
    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1 / 6:
        return p + (q - p)*6*t
    if t < 1 / 2:
        return q
    if t < 2 / 3:
        return p + (q - p)*(2 / 3 - t)*6
    return p

