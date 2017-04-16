"""
    @package segmentation
    Image segmentation 
"""
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




    float gaussianDeviation=ui->cannyGaussianDeviationBox->value();
    int32_t gaussianFilterSize=floor(gaussianDeviation*3.0f); // NVidia standard
    float *bwImg=getBWFloatArrayFromImage(bmpData,width,height);
    float *gaussianImg=applyGaussianBlurToSingleChannelFloatArray(bwImg,width,height,gaussianFilterSize,gaussianDeviation);

    // Perform convolution (2 filters, accX and accY)

    float *gradient=(float*)malloc(width*height*sizeof(float));
    float *gradientAtan2=(float*)malloc(width*height*sizeof(float)); // In degs

    // Modify Sobel algorithm, too!

    for(int32_t y=0;y<height;y++)
    {
        int32_t offset=y*width;
        for(int32_t x=0;x<width;x++)
        {
            float accXValueSum=0.0f;
            float accYValueSum=0.0f;

            int32_t leftX=x-1;
            int32_t rightX=x+1;
            int32_t topY=y-1;
            int32_t bottomY=y+1;

            bool hasTop=topY>=0;
            bool hasBottom=bottomY<height;
            bool hasLeft=leftX>=0;
            bool hasRight=rightX<width;
            float factor;

            if(hasLeft)
            {
                if(hasTop)
                {
                    // X accumulator
                    factor=-1.0f;
                    accXValueSum+=gaussianImg[topY*width+leftX]*factor;
                    // Y accumulator
                    factor=-1.0f;
                    accYValueSum+=gaussianImg[topY*width+leftX]*factor;
                }
                else
                {
                    // Extend the image by 1 pixel on each side and using the outmost pixels in order to
                    // avoid false positives on the borders of the image

                    // X accumulator
                    factor=-1.0f;
                    accXValueSum+=gaussianImg[y*width+leftX]*factor;
                    // Y accumulator
                    factor=-1.0f;
                    accYValueSum+=gaussianImg[y*width+leftX]*factor;
                }
                if(hasBottom)
                {
                    // X accumulator
                    factor=-1.0f;
                    accXValueSum+=gaussianImg[bottomY*width+leftX]*factor;
                    // Y accumulator
                    factor=1.0f;
                    accYValueSum+=gaussianImg[bottomY*width+leftX]*factor;
                }
                else
                {
                    // X accumulator
                    factor=-1.0f;
                    accXValueSum+=gaussianImg[y*width+leftX]*factor;
                    // Y accumulator
                    factor=1.0f;
                    accYValueSum+=gaussianImg[y*width+leftX]*factor;
                }
                // X accumulator
                factor=-2.0f;
                accXValueSum+=gaussianImg[y*width+leftX]*factor;
            }
            else
            {
                if(hasTop)
                {
                    // X accumulator
                    factor=-1.0f;
                    accXValueSum+=gaussianImg[topY*width+x]*factor;
                    // Y accumulator
                    factor=-1.0f;
                    accYValueSum+=gaussianImg[topY*width+x]*factor;
                }
                else
                {
                    // Extend the image by 1 pixel on each side and using the outmost pixels in order to
                    // avoid false positives on the borders of the image

                    // X accumulator
                    factor=-1.0f;
                    accXValueSum+=gaussianImg[y*width+x]*factor;
                    // Y accumulator
                    factor=-1.0f;
                    accYValueSum+=gaussianImg[y*width+x]*factor;
                }
                if(hasBottom)
                {
                    // X accumulator
                    factor=-1.0f;
                    accXValueSum+=gaussianImg[bottomY*width+x]*factor;
                    // Y accumulator
                    factor=1.0f;
                    accYValueSum+=gaussianImg[bottomY*width+x]*factor;
                }
                else
                {
                    // X accumulator
                    factor=-1.0f;
                    accXValueSum+=gaussianImg[y*width+x]*factor;
                    // Y accumulator
                    factor=1.0f;
                    accYValueSum+=gaussianImg[y*width+x]*factor;
                }
                // X accumulator
                factor=-2.0f;
                accXValueSum+=gaussianImg[y*width+x]*factor;
            }
            if(hasRight)
            {
                if(hasTop)
                {
                    // X accumulator
                    factor=1.0f;
                    accXValueSum+=gaussianImg[topY*width+rightX]*factor;
                    // Y accumulator
                    factor=-1.0f;
                    accYValueSum+=gaussianImg[topY*width+rightX]*factor;
                }
                else
                {
                    // X accumulator
                    factor=1.0f;
                    accXValueSum+=gaussianImg[y*width+rightX]*factor;
                    // Y accumulator
                    factor=-1.0f;
                    accYValueSum+=gaussianImg[y*width+rightX]*factor;
                }
                if(hasBottom)
                {
                    // X accumulator
                    factor=1.0f;
                    accXValueSum+=gaussianImg[bottomY*width+rightX]*factor;
                    // Y accumulator
                    factor=1.0f;
                    accYValueSum+=gaussianImg[bottomY*width+rightX]*factor;
                }
                else
                {
                    // X accumulator
                    factor=1.0f;
                    accXValueSum+=gaussianImg[y*width+rightX]*factor;
                    // Y accumulator
                    factor=1.0f;
                    accYValueSum+=gaussianImg[y*width+rightX]*factor;
                }
                // X accumulator
                factor=2.0f;
                accXValueSum+=gaussianImg[y*width+rightX]*factor;
            }
            else
            {
                if(hasTop)
                {
                    // X accumulator
                    factor=1.0f;
                    accXValueSum+=gaussianImg[topY*width+x]*factor;
                    // Y accumulator
                    factor=-1.0f;
                    accYValueSum+=gaussianImg[topY*width+x]*factor;
                }
                else
                {
                    // X accumulator
                    factor=1.0f;
                    accXValueSum+=gaussianImg[y*width+x]*factor;
                    // Y accumulator
                    factor=-1.0f;
                    accYValueSum+=gaussianImg[y*width+x]*factor;
                }
                if(hasBottom)
                {
                    // X accumulator
                    factor=1.0f;
                    accXValueSum+=gaussianImg[bottomY*width+x]*factor;
                    // Y accumulator
                    factor=1.0f;
                    accYValueSum+=gaussianImg[bottomY*width+x]*factor;
                }
                else
                {
                    // X accumulator
                    factor=1.0f;
                    accXValueSum+=gaussianImg[y*width+x]*factor;
                    // Y accumulator
                    factor=1.0f;
                    accYValueSum+=gaussianImg[y*width+x]*factor;
                }
                // X accumulator
                factor=2.0f;
                accXValueSum+=gaussianImg[y*width+x]*factor;
            }
            if(hasTop)
            {
                // Y accumulator
                factor=-2.0f;
                accYValueSum+=gaussianImg[topY*width+x]*factor;
            }
            else
            {
                // Y accumulator
                factor=-2.0f;
                accYValueSum+=gaussianImg[y*width+x]*factor;
            }
            if(hasBottom)
            {
                // Y accumulator
                factor=2.0f;
                accYValueSum+=gaussianImg[bottomY*width+x]*factor;
            }
            else
            {
                // Y accumulator
                factor=2.0f;
                accYValueSum+=gaussianImg[y*width+x]*factor;
            }
            // The pixel in the center has 0.0f as its factor for both filters.

            int32_t pos=offset+x;

            // Result
            gradient[pos]=sqrt(pow(accXValueSum,2.0f)+pow(accYValueSum,2.0f));
            gradientAtan2[pos]=atan2(accXValueSum,accYValueSum);
        }
    }

    float *preResult=(float*)malloc(width*height*sizeof(float));

    for(int32_t y=0;y<height;y++)
    {
        int32_t offset=y*width;
        for(int32_t x=0;x<width;x++)
        {
            int32_t leftX=x-1;
            int32_t rightX=x+1;
            int32_t topY=y-1;
            int32_t bottomY=y+1;

            bool hasTop=topY>=0;
            bool hasBottom=bottomY<height;
            bool hasLeft=leftX>=0;
            bool hasRight=rightX<width;

            int32_t pos=offset+x;
            float angle=gradientAtan2[pos];

            int rAngle=(int)round(angle/(0.25f*((float)M_PI))); // 45 degrees
            if(rAngle<0)
                rAngle=4+rAngle;
            bool eastWest=rAngle==0||rAngle==4; // The first section is split (one half on each end)
            bool northEastSouthWest=rAngle==1;
            bool northSouth=rAngle==2;
            bool northWestSouthEast=rAngle==3;


            float thisPixelValue=gradient[y*width+x];
            if(eastWest)
            {
                float neighborPixelValue1=hasTop?gradient[topY*width+x]:gradient[y*width+x];
                float neighborPixelValue2=hasBottom?gradient[bottomY*width+x]:gradient[y*width+x];
                if(thisPixelValue>neighborPixelValue1&&thisPixelValue>neighborPixelValue2)
                    preResult[pos]=thisPixelValue;
                else
                    preResult[pos]=0.0f;
            }
            else if(northEastSouthWest)
            {
                float neighborPixelValue1=hasLeft&&hasTop?gradient[topY*width+leftX]:(hasLeft?gradient[y*width+leftX]:(hasTop?gradient[topY*width+x]:gradient[y*width+x]));
                float neighborPixelValue2=hasRight&&hasBottom?gradient[bottomY*width+rightX]:(hasRight?gradient[y*width+rightX]:(hasBottom?gradient[bottomY*width+x]:gradient[y*width+x]));
                if(thisPixelValue>neighborPixelValue1&&thisPixelValue>neighborPixelValue2)
                    preResult[pos]=thisPixelValue;
                else
                    preResult[pos]=0.0f;
            }
            else if(northSouth)
            {
                float neighborPixelValue1=hasLeft?gradient[y*width+leftX]:gradient[y*width+x];
                float neighborPixelValue2=hasRight?gradient[y*width+rightX]:gradient[y*width+x];
                if(thisPixelValue>neighborPixelValue1&&thisPixelValue>neighborPixelValue2)
                    preResult[pos]=thisPixelValue;
                else
                    preResult[pos]=0.0f;
            }
            else if(northWestSouthEast)
            {
                float neighborPixelValue1=hasRight&&hasTop?gradient[topY*width+rightX]:(hasRight?gradient[y*width+rightX]:(hasTop?gradient[topY*width+x]:gradient[y*width+x]));
                float neighborPixelValue2=hasLeft&&hasBottom?gradient[bottomY*width+leftX]:(hasLeft?gradient[y*width+leftX]:(hasBottom?gradient[bottomY*width+x]:gradient[y*width+x]));
                if(thisPixelValue>neighborPixelValue1&&thisPixelValue>neighborPixelValue2)
                    preResult[pos]=thisPixelValue;
                else
                    preResult[pos]=0.0f;
            }
        }
    }

    float lowTreshold=ui->cannyLowTresholdBox->value();
    float highTreshold=ui->cannyHighTresholdBox->value();

    for(int32_t y=0;y<height;y++)
    {
        int32_t offset=y*width;
        for(int32_t x=0;x<width;x++)
        {
            float value=preResult[offset+x];
            float newValue;
            if(value<lowTreshold)
                newValue=0.0f;
            else if(value<highTreshold)
                newValue=0.5f;
            else // if(value>=highTreshold)
                newValue=1.0f;
            preResult[offset+x]=newValue;
        }
    }

    float *result=(float*)malloc(width*height*sizeof(float));

    for(int32_t y=0;y<height;y++)
    {
        int32_t offset=y*width;
        for(int32_t x=0;x<width;x++)
        {
            float value=preResult[offset+x];
            if(value==0.0f) // No edge; do not keep
                continue;
            else if(value==1.0f) // Strong edge; keep
                goto Keep;

            // Weak edge; decide whether to keep it (if at least one neighboring pixel is a strong edge)

            {
                int32_t leftX=x-1;
                int32_t rightX=x+1;
                int32_t topY=y-1;
                int32_t bottomY=y+1;

                bool hasTop=topY>=0;
                bool hasBottom=bottomY<height;
                bool hasLeft=leftX>=0;
                bool hasRight=rightX<width;
                // Use x==1.0f, not x>0.0f here!
                if(hasLeft)
                {
                    if(preResult[y*width+leftX]==1.0f)
                        goto Keep;
                    if(hasTop)
                    {
                        if(preResult[topY*width+leftX]==1.0f)
                            goto Keep;
                    }
                    if(hasBottom)
                    {
                        if(preResult[bottomY*width+leftX]==1.0f)
                            goto Keep;
                    }
                }
                if(hasRight)
                {
                    if(preResult[y*width+rightX]==1.0f)
                        goto Keep;
                    if(hasTop)
                    {
                        if(preResult[topY*width+rightX]==1.0f)
                            goto Keep;
                    }
                    if(hasBottom)
                    {
                        if(preResult[bottomY*width+rightX]==1.0f)
                            goto Keep;
                    }
                }
                if(hasTop)
                {
                    if(preResult[topY*width+x]==1.0f)
                        goto Keep;
                }
                if(hasBottom)
                {
                    if(preResult[bottomY*width+x]==1.0f)
                        goto Keep;
                }
                // Do not keep
                result[offset+x]=0.0f;
                continue;
            }
            Keep:
            // Keep
            result[offset+x]=1.0f;
        }
    }