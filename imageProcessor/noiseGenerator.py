"""
    @package noiseGenerator
    Generate noise for image
"""

from PIL import Image
import math
import random
import numpy
from PyQt5.QtCore import QCoreApplication

def impulsNoise(pixels, size, colorModelTag, impulsP, noiseLvl):
    noisepixel = int(size[0] * size[1] * noiseLvl / 100)
    for i in range(noisepixel):
        QCoreApplication.processEvents()
        x = random.choice(range(0, size[0])) # случайная координата х от 0 до width
        y = random.choice(range(0, size[1])) # случайная координата y от 0 до heigth
        currentColor = pixels[x, y]
        randomValue = random.choice(range(0, 100))
        if colorModelTag == 'RGB':
            if randomValue < impulsP:
                value = (0, 0, 0)
            else:
                value = (255, 255, 255)
        if colorModelTag == 'YUV':
            if randomValue < impulsP:
                value = (0, currentColor[1], currentColor[2])
            else:
                value = (255, currentColor[1], currentColor[2])
        if colorModelTag == 'HSL':
            if randomValue < impulsP:
                currentColor -= 180
                currentColor = currentColor if currentColor > 0 else 360 + currentColor
            else:
                currentColor += 180
                currentColor = currentColor if currentColor > 360 else currentColor - 360
            value = (currentColor, currentColor[1], currentColor[2])
        pixels[x, y] = value