import numpy as np
import cv2 as cv2
from get_Fov_Mask import *
from wavelet import findGoodResolutionForWavelet
from kirsch_egdes import *
from image_reconstruct import imreconstruct
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import scipy.signal as signal
import skimage as sk


# pierre amir


def getLesions(rgbImgOrig, showRes, removeON, onY, onX):
    # % Parameters
    winOnRatio = np.array([1/8, 1/8])

    # % resize
    height, width, channels = rgbImgOrig.shape
    origSize = [height, width]
    newSize = [750, round(750*(origSize[1]/origSize[0]))]
    newSize = findGoodResolutionForWavelet(newSize)    
    imgRGB = cv2.resize(rgbImgOrig, newSize)
    # extract green channel to work with kirsch edges
    imgG = imgRGB[:, :, 1]
    # % change colour plane
    imgHSV = sk.color.rgb2hsv(imgRGB)
    # extract value channel ( brightnss) 
    imgV = imgHSV[:, :, 2]
    # multiply by 255 to get values between 0 and 255
    imgV8 = imgV * 255
    imgV8 = imgV8.astype(np.uint8)

  
    # %--- Remove OD region
    if(removeON):
        # % get ON window
        # preprare the size of the window
        onY = onY * newSize[0]/origSize[0]
        onX = onX * newSize[1]/origSize[1]
        onX = round(onX)
        onY = round(onY)
        winOnSize = np.round(winOnRatio * newSize)

        # % remove ON window from imgTh
        winOnCoordY = np.array([onY-winOnSize[0], onY+winOnSize[0]])
        winOnCoordX = np.array([onX-winOnSize[1], onX+winOnSize[1]])
    
        if(winOnCoordY[0] < 1):
            winOnCoordY[0] = 1
        if(winOnCoordX[0] < 1):
            winOnCoordX[0] = 1
        if(winOnCoordY[1] > newSize[0]):
            winOnCoordY[1] = newSize[0]
        if(winOnCoordX[1] > newSize[1]):
            winOnCoordX[1] = newSize[1]
    # %     imgThNoOD = imgTh;
        winOnCoordY.astype(np.uint8)
        winOnCoordX.astype(np.uint8)

    # % Create FOV mask
   # make a mask of the filed of view to start to segment the background details from the background
    imgFovMask = getFovMask(imgV8, 1, 30)
    # HIDE THE BRRIGHT REGION IN THE IMAGE BY A MASK
    imgFovMask[int(winOnCoordY[0]):int(winOnCoordY[1]),
             int(winOnCoordX[0]):int(winOnCoordX[1])] = 0
    
    # %--- fixed threshold using median Background (with reconstruction)
    kernal_size = round(newSize[0]/30)
    # USE MEDIAN FILTER TO BLUR THE IMAGE TO DECREASE THE EDGES IN THE IMAGE AND MAKE DETAILS MORE OBVIOUS
    medBg = signal.medfilt2d(imgV8, round(newSize[0]/30))
    # %reconstruct bg
    maskImg = imgV8
    maskImg = maskImg
    # THREESHOLD THE VALUE CHANNNEL FROM THE IMAGE ACCORDING THE MEDIAN FILTERS
    pxLbl = maskImg < medBg
    maskImg[pxLbl] = medBg[pxLbl]
    #
    medRestored = sk.morphology.reconstruction(medBg, maskImg)
    # % subtract, remove fovMask and threshold
    #AFTER REMOVE VESSELS FROM THE BACGROUND   
    subImg = imgV8 - medRestored
    subImg = subImg * imgFovMask
    subImg[subImg < 0] = 0
    imgThNoOD = subImg.astype(np.int8) > 0
    # %---

    # %--- Calculate edge strength of lesions
    # NOW WE WORK ON THE GREEN CHANNEL FROM THE RGBIMAGE TO GET THE EDGE STRENGTH OF THE LESIONS
    imgKirsch = kirschEdges(imgG)
    img0 = imgG * (imgThNoOD == 0) # HERE WE GET THE VESSELES FROM THE GREEN CHANNEL BY INVERTING THE KERNAL OF NOOD
    img0recon = sk.morphology.reconstruction(img0, imgG)
    img0Kirsch = kirschEdges(img0recon)
#HERRE WE MAKE A MASK THAT DETECT THE NON VESSELES ELEMENT IN THE IMAGE
# WE MADE THE MASK BY SUBTRACTING THE VESSELS MASK FROM THE KERSH 
    imgEdgeNoMask = imgKirsch - img0Kirsch
    
    # %---
   # HERE WE SEGMENT THE EXUDATES FROM THE BACK GROUND
    imgEdge = imgFovMask * imgEdgeNoMask
    
       
    #     %--- Calculate edge strength for each lesion candidate (Matlab2008)
    # REGIONNING OF THE LESIONS AND SIBISTITUTE WITH ITS COOORDINATES IN ZEROS MATRIX
    lesCandImg = np.zeros_like(imgEdge)
    lblImg = label(imgThNoOD, connectivity=2)
    lesCand = regionprops(lblImg)

    for idxLes in range(0, len(lesCand)):
        pxIdxList = lesCand[idxLes].coords
        pxIdxList=pxIdxList[:,0],pxIdxList[:,1]
        lesCandImg[pxIdxList] = np.sum(imgEdge[pxIdxList]) / len(pxIdxList)

        # % RETURN THE IMAGE TO THE ORIGINAL SIZE AND INTERPULATE WITH NEAREST NEIGHBOUR TO DECREASE 
        # THE COMPUTATIONAL COST OF THE ALGORITHM
    lesCandImg = cv2.resize(lesCandImg, origSize,
                            interpolation=cv2.INTER_NEAREST)


  #PLOT THE RESULT
    if(showRes):
    
        fig = plt.figure()
        # % plot original image
        plt.subplot(1, 2, 1)
        plt.imshow(imgRGB)
        # % plot segmented image  
        plt.subplot(1, 2, 2)
        plt.imshow(lesCandImg)
        plt.show()
        
    return lesCandImg
