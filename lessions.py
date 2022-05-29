import numpy as np
import cv2 as cv2
from get_Fov_Mask import *
# pierre amir

def getLesions(rgbImgOrig, showRes, removeON, onY, onX):
    # % Parameters
    winOnRatio = np.array([1/8, 1/8])

    # % resize
    height, width, channels = rgbImgOrig.shape
    origSize = (height, width, channels)
    newSize = (750, round(750*(origSize[1]/origSize[0])))
    newSize = findGoodResolutionForWavelet(newSize)    # pierre
    imgRGB = cv2.resize(rgbImgOrig, newSize)
    imgG = imgRGB[:, :, 1]
    # % change colour plane
    imgHSV = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2HSV)
    imgV = imgHSV[:, :, 2]
    imgV8 = int(imgV*255)

    # %--- Remove OD region
    if(removeON):
        # % get ON window
        onY = onY * newSize[0]/origSize[0]
        onX = onX * newSize[1]/origSize[1]
        onX = round(onX)
        onY = round(onY)
        winOnSize = round(np.dot(winOnRatio, newSize))
        # % remove ON window from imgTh
        winOnCoordY = [onY-winOnSize[0], onY+winOnSize[0]]
        winOnCoordX = [onX-winOnSize[1], onX+winOnSize[1]]
        if(winOnCoordY[0] < 1):
            winOnCoordY[0] = 1
        if(winOnCoordX[0] < 1):
            winOnCoordX[0] = 1
        if(winOnCoordY[1] > newSize[0]):
            winOnCoordY[1] = newSize[0]
        if(winOnCoordX[1] > newSize[1]):
            winOnCoordX[1] = newSize[1]
    # %     imgThNoOD = imgTh;
    # %     imgThNoOD(winOnCoordY[0]:winOnCoordY[1], winOnCoordX[0]:winOnCoordX[1]) = 0;
    #     end
    # %---

    # % Create FOV mask
    imgFovMask = getFovMask(imgV8, 1, 30)
    imgFovMask[winOnCoordY[0]:winOnCoordY[1],
               winOnCoordX[0]:winOnCoordX[1]] = 0

    # %--- fixed threshold using median Background (with reconstruction)
    medBg = float(
        medfilt2(imgV8, (round(newSize[0]/30), round(newSize[0]/30))))
    # %reconstruct bg
    maskImg = float(imgV8)
    pxLbl = maskImg < medBg
    maskImg[pxLbl] = medBg[pxLbl]
    medRestored = imreconstruct(medBg, maskImg)
    # % subtract, remove fovMask and threshold
    subImg = float(imgV8) - float(medRestored)
    subImg = np.dot(subImg, float(imgFovMask))
    subImg[subImg < 0] = 0
    imgThNoOD = int(subImg) > 0
    # %---

    # %--- Calculate edge strength of lesions
    imgKirsch = kirschEdges(imgG)
    img0 = np.dot(imgG(imgThNoOD == 0))
    img0recon = imreconstruct(img0, imgG)
    img0Kirsch = kirschEdges(img0recon)
    # % edge strength map
    imgEdgeNoMask = imgKirsch - img0Kirsch

    # %---
    # % remove mask and ON (leave vessels)
    imgEdge = np.dot(float(imgFovMask), imgEdgeNoMask)

    #     %--- Calculate edge strength for each lesion candidate (Matlab2008)
    lesCandImg = np.zeros(newSize)
    lblImg = bwlabel(imgThNoOD, 8)
    lesCand = regionprops(lblImg, 'PixelIdxList')

    for idxLes in range(1, len(lesCand)):
        pxIdxList = lesCand[idxLes].PixelIdxList
        lesCandImg[pxIdxList] = sum(imgEdge(pxIdxList)) / len(pxIdxList)
   
        # % resize back
    lesCandImg = cv2.resize(
        lesCandImg, origSize[0:1], interpolation=cv2.INTER_NEAREST)

    if(showRes):
        pass
        # figure(442);
        # imagesc( rgbImgOrig );
        # figure(446);
        # imagesc( lesCandImg );

    return 0  # lesCandImg
