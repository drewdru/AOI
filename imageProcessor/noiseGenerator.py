"""
    @package noiseGenerator
    Generate noise for image
"""

from PIL import Image
import math
import random
import numpy
from PyQt5.QtCore import QCoreApplication

def fixColorChannelRange(colorValue, maxValue=255):
    minValue = 0
    if colorValue > maxValue:
        colorValue -= maxValue
    if colorValue < minValue:
        colorValue += maxValue
    return colorValue

def impulsNoise(pixels, size, colorModelTag, currentImageChannelIndex, impulsP, noiseLvl):
    noisepixel = int(size[0] * size[1] * noiseLvl / 100)
    for i in range(noisepixel):
        QCoreApplication.processEvents()
        x = random.choice(range(0, size[0]))
        y = random.choice(range(0, size[1]))
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

        if colorModelTag == 'HSL':
            if currentImageChannelIndex == 0:
                colorValue = currentColor[0]
                if randomValue < impulsP:
                    colorValue -= 180
                    anotherColors = 0
                else:
                    colorValue += 180
                    anotherColors = 100
                colorValue = fixColorChannelRange(colorValue, 360)
                value = (colorValue, anotherColors, anotherColors)
            elif currentImageChannelIndex == 1:
                colorValue = currentColor[0]
                if randomValue < impulsP:
                    colorValue -= 180
                else:
                    colorValue += 180
                colorValue = fixColorChannelRange(colorValue, 360)
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

# fix noise https://dsp.stackexchange.com/questions/13895/which-domain-used-for-denoising-additive-and-multiplicative-noises
def getAdditiveValue(currentColor, maxValue, deviation):
    deviation = int(deviation)
    color = currentColor + random.choice(range(-deviation, deviation))
    color = fixColorChannelRange(color, maxValue)
    return color

def additiveNoise(pixels, size, colorModelTag, currentImageChannelIndex, deviation, noiseLvl):
    noisepixel = int(size[0] * size[1] * noiseLvl / 100)
    for i in range(noisepixel):
        QCoreApplication.processEvents()
        x = random.choice(range(0, size[0]))
        y = random.choice(range(0, size[1]))
        currentColor = pixels[x, y]
        if colorModelTag == 'RGB' or colorModelTag == 'YUV':
            deviationValue = 255 * deviation / 100
            if currentImageChannelIndex == 0:
                rand1 = getAdditiveValue(currentColor[0], 255, deviationValue)
                rand2 = getAdditiveValue(currentColor[1], 255, deviationValue)
                rand3 = getAdditiveValue(currentColor[2], 255, deviationValue)

                value = (rand1, rand2, rand3)
            else:
                value = [currentColor[0], currentColor[1], currentColor[2]]
                value[currentImageChannelIndex - 1] = getAdditiveValue(
                    currentColor[currentImageChannelIndex - 1],
                    255,
                    deviationValue)
                value = tuple(value)

        if colorModelTag == 'HSL':
            if currentImageChannelIndex == 0:
                deviationValue1 = 360 * deviation / 100
                rand1 = getAdditiveValue(currentColor[0], 360, deviationValue1)
                deviationValue2 = 100 * deviation / 100
                rand2 = getAdditiveValue(currentColor[1], 100, deviationValue2)
                rand3 = getAdditiveValue(currentColor[2], 100, deviationValue2)

                value = (rand1, rand2, rand3)
            elif currentImageChannelIndex == 1:
                deviationValue = 360 * deviation / 100
                randColor = getAdditiveValue(currentColor[0], 360, deviationValue)
                value = (randColor, currentColor[1], currentColor[2])
            else:
                deviationValue = 100 * deviation / 100
                value = [currentColor[0], currentColor[1], currentColor[2]]
                value[currentImageChannelIndex - 1] = getAdditiveValue(
                    currentColor[currentImageChannelIndex - 1],
                    100,
                    deviationValue)
                value = tuple(value)

        pixels[x, y] = value



# fix noise https://dsp.stackexchange.com/questions/13895/which-domain-used-for-denoising-additive-and-multiplicative-noises
def getMultiplicativeValue(currentColor, maxValue, kmin, kmax):
    color = currentColor * random.choice(range(int(kmin), int(kmax)))
    color = 0 if abs(color) > 2 * maxValue else color
    color = fixColorChannelRange(color, maxValue)
    return color

def multiplicativeNoise(pixels, size, colorModelTag, currentImageChannelIndex, kmin, kmax, noiseLvl):
    noisepixel = int(size[0] * size[1] * noiseLvl / 100)
    for i in range(noisepixel):
        QCoreApplication.processEvents()
        x = random.choice(range(0, size[0]))
        y = random.choice(range(0, size[1]))
        currentColor = pixels[x, y]
        if colorModelTag == 'RGB' or colorModelTag == 'YUV':
            if currentImageChannelIndex == 0:
                rand1 = getMultiplicativeValue(currentColor[0], 255, kmin, kmax)
                rand2 = getMultiplicativeValue(currentColor[1], 255, kmin, kmax)
                rand3 = getMultiplicativeValue(currentColor[2], 255, kmin, kmax)

                value = (rand1, rand2, rand3)
            else:
                value = [currentColor[0], currentColor[1], currentColor[2]]
                value[currentImageChannelIndex - 1] = getMultiplicativeValue(
                    currentColor[currentImageChannelIndex - 1],
                    255,
                    kmin,
                    kmax)
                value = tuple(value)

        if colorModelTag == 'HSL':
            if currentImageChannelIndex == 0:
                rand1 = getMultiplicativeValue(currentColor[0], 360, kmin, kmax)
                rand2 = getMultiplicativeValue(currentColor[1], 100, kmin, kmax)
                rand3 = getMultiplicativeValue(currentColor[2], 100, kmin, kmax)

                value = (rand1, rand2, rand3)
            elif currentImageChannelIndex == 1:
                randColor = getMultiplicativeValue(currentColor[0], 360, kmin, kmax)
                value = (randColor, currentColor[1], currentColor[2])
            else:
                value = [currentColor[0], currentColor[1], currentColor[2]]
                value[currentImageChannelIndex - 1] = getMultiplicativeValue(
                    currentColor[currentImageChannelIndex - 1],
                    100,
                    kmin,
                    kmax)
                value = tuple(value)

        pixels[x, y] = value
