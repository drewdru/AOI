/**
 * Change an image hue
 * 
 * @param value: The hue value
 * @param isOriginalImage: The value for choose original or processing Image
 */
function changeHue(value, isOriginalImage) {
    colorCorrectorController.changeHue(value, isOriginalImage);
}

/**
 * Convert image to grayscale
 * 
 * @param isOriginalImage: The value for choose original or processing Image
 */
function toGrayscale(isOriginalImage) {
    colorCorrectorController.toGrayscale(isOriginalImage);
}

/**
 * Change color model and channels
 * 
 * @param colorModelTag: The color model tag
 * @param currentImageChannelIndex: The index of current image channel
 */
function changeColorModel(colorModelTag, currentImageChannelIndex) {
    colorCorrectorController.changeColorModel(colorModelTag, currentImageChannelIndex);
}