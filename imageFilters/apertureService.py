def getAperturePosition(x, y, imgSize, i, j, filterSize):
    pixelPosX = x + j - filterSize[0] / 2.0
    pixelPosY = y + i - filterSize[1] / 2.0
    if pixelPosX < 0:
        pixelPosX += filterSize[0] / 2.0
    if pixelPosY < 0:
        pixelPosY += filterSize[1] / 2.0
    if pixelPosX > imgSize[0] or pixelPosY > imgSize[1]:
        return -1, -1
    if pixelPosX == imgSize[0]:
        pixelPosX = imgSize[0] - (filterSize[0] / 2.0) - 1
    if pixelPosY == imgSize[1]:
        pixelPosY = imgSize[1] - (filterSize[1] / 2.0) - 1
    return (int(pixelPosX), int(pixelPosY))

def getAperturePointGenerator(imgSize, filterSize):
    for x in range(imgSize[0]):
        for y in range(imgSize[1]):
            for i in range(filterSize[0]):
                for j in range(filterSize[1]):
                    pixelPosX, pixelPosY = getAperturePosition(
                        x, y,
                        imgSize,
                        i, j,
                        filterSize)
                    if pixelPosX == -1 or pixelPosY == -1:
                        continue
                    yield pixelPosX, pixelPosY

def getApertureMatrixGenerator(imgSize, filterSize):
    for x in range(imgSize[0]):
        for y in range(imgSize[1]):
            apertureMatrix = []
            for i in range(filterSize[0]):
                matrixLine = []
                for j in range(filterSize[0]):
                    pixelPosX, pixelPosY = getAperturePosition(
                        x, y,
                        imgSize,
                        i, j,
                        filterSize)
                    if pixelPosX == -1 or pixelPosY == -1:
                        continue
                    matrixLine.append((pixelPosX, pixelPosY))
                apertureMatrix.append(matrixLine)
            yield (x, y, apertureMatrix)

# Example
# aperture = apertureGenerator([200, 200], 3)
# print(aperture)
# for i, j in aperture:
#     print(i, j)
