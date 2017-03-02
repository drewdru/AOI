"""
    @package noiseGenerator
    Generate noise for image
"""

from PIL import Image
import math
import random
import numpy
from PyQt5.QtCore import QCoreApplication

def impulsNoise(pixels, size, colorModelTag, currentImageChannelIndex, impulsP, noiseLvl):
    noisepixel = int(size[0] * size[1] * noiseLvl / 100)
    for i in range(noisepixel):
        QCoreApplication.processEvents()
        x = random.choice(range(0, size[0])) # случайная координата х от 0 до width
        y = random.choice(range(0, size[1])) # случайная координата y от 0 до heigth
        currentColor = pixels[x, y]
        randomValue = random.choice(range(0, 100))
        if colorModelTag == 'RGB':
            if currentImageChannelIndex == 0:
                if randomValue < impulsP:
                    value = (0, 0, 0)
                else:
                    value = (255, 255, 255)
            else:
                if randomValue < impulsP:
                    value = [currentColor[0], currentColor[1], currentColor[2]]
                    value[currentImageChannelIndex - 1] = 0
                else:
                    value = [currentColor[0], currentColor[1], currentColor[2]]
                    value[currentImageChannelIndex - 1] = 255
                value = tuple(value)

        if colorModelTag == 'YUV':
            if currentImageChannelIndex == 0:
                if randomValue < impulsP:
                    value = (0, currentColor[1], currentColor[2])
                else:
                    value = (255, currentColor[1], currentColor[2])
            else:
                if randomValue < impulsP:
                    value = [currentColor[0], currentColor[1], currentColor[2]]
                    value[currentImageChannelIndex - 1] = 0
                else:
                    value = [currentColor[0], currentColor[1], currentColor[2]]
                    value[currentImageChannelIndex - 1] = 255
                value = tuple(value)
        if colorModelTag == 'HSL':
            if currentImageChannelIndex <= 1 :
                colorValue = currentColor[0]
                if randomValue < impulsP:
                    colorValue -= 180
                else:
                    colorValue += 180
                if colorValue > 360:
                    colorValue -= 360
                if colorValue < 0:
                    colorValue += 360
                value = (colorValue, currentColor[1], currentColor[2])
            else:
                if randomValue < impulsP:
                    value = [currentColor[0], currentColor[1], currentColor[2]]
                    value[currentImageChannelIndex - 1] = 0
                else:
                    value = [currentColor[0], currentColor[1], currentColor[2]]
                    value[currentImageChannelIndex - 1] = 100
                value = tuple(value)
        pixels[x, y] = value