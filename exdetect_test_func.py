from lessions import getLesions
import cv2



def exDetect( rgbImgOrig= cv2.imread( './img_ex_test.jpg' ), removeON= 1, onY= 905, onX = 290 ):
  
    showRes = 1
   
    imgProb = getLesions( rgbImgOrig, showRes, removeON, onY, onX )

    return imgProb