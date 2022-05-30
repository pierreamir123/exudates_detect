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
    newSize = findGoodResolutionForWavelet(newSize)    # pierre
    imgRGB = cv2.resize(rgbImgOrig, newSize)
    imgG = imgRGB[:, :, 1]
    # % change colour plane
    imgHSV = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2HSV)
    imgV = imgHSV[:, :, 2]
    imgV8 = np.multiply(imgV , 255)
    imgV8 = imgV8.astype(np.int8)        
    # %--- Remove OD region
    if(removeON):
        # % get ON window
        onY = onY * newSize[0]/origSize[0]
        onX = onX * newSize[1]/origSize[1]
        onX = round(onX)
        onY = round(onY)
        winOnSize = np.round(np.multiply(winOnRatio, newSize))

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
        winOnCoordY.astype(np.int16)
        winOnCoordX.astype(np.int16)   

    # % Create FOV mask

    imgFovMask = getFovMask(imgV8, 1, 30)
    imgFovMask[int(winOnCoordY[0]):int(winOnCoordY[1]),int(winOnCoordX[0]):int(winOnCoordX[1])] = 0

    # %--- fixed threshold using median Background (with reconstruction)
    kernal_size = round(newSize[0]/30)
    print("kernal_size",kernal_size)
    medBg = signal.medfilt2d(imgV8, round(newSize[0]/30) )
    # %reconstruct bg
    maskImg = imgV8
    maskImg = maskImg.astype(np.float32)
    pxLbl = maskImg < medBg
    maskImg[pxLbl] = medBg[pxLbl]
    medRestored = sk.morphology.reconstruction(medBg, maskImg)
    # % subtract, remove fovMask and threshold
    subImg = imgV8.astype(np.float32) - medRestored.astype(np.float32)
    subImg = subImg * imgFovMask.astype(np.float32) 
    subImg[subImg < 0] = 0
    imgThNoOD = subImg.astype(np.int16) > 0
    # %---

    # %--- Calculate edge strength of lesions
    imgKirsch = kirschEdges(imgG)
    img0 =  imgG *(imgThNoOD == 0)
    img0recon = sk.morphology.reconstruction(img0, imgG)
    img0Kirsch = kirschEdges(img0recon)
    # % edge strength map
    imgEdgeNoMask = imgKirsch - img0Kirsch

    # %---
    # % remove mask and ON (leave vessels)
    imgEdge = imgFovMask.astype(np.float32) * imgEdgeNoMask

    #     %--- Calculate edge strength for each lesion candidate (Matlab2008)
    lesCandImg = np.zeros(newSize)
    lblImg = label(imgThNoOD, connectivity=2)
    lesCand = regionprops(lblImg)

    for idxLes in range(1, len(lesCand)):
        pxIdxList = lesCand[idxLes].coords
        print("pxIdxList",pxIdxList)
        lesCandImg[pxIdxList] = np.sum(imgEdge[pxIdxList]) / len(pxIdxList)
   
        # % resize back
    lesCandImg = cv2.resize(lesCandImg, origSize, interpolation=cv2.INTER_NEAREST)

    if(showRes):
        pass
        fig, ax = plt.subplots(1, 2, sharex='col', sharey='row')
        plt.subplot(111)
        plt.imshow(rgbImgOrig)
        plt.subplot(121)
        plt.imshow(lesCandImg , cmap='gray')
        plt.show()
    return lesCandImg




