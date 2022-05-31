from lessions import getLesions
import cv2
import matplotlib.pyplot as plt



def exDetect( rgbImgOrig, removeON= 1, onY= 905, onX = 290 ):
  
    showRes = 1
    
    imgProb = getLesions( rgbImgOrig , showRes, removeON, onY, onX )

    return imgProb