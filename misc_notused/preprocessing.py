import numpy as np
import cv2 as cv2



def  preprocessMed( imgPlane, meanTgt, stdTgt ):
    height, width ,channels = imgPlane.shape
    medFiltWin_array = (height*0.04 ,height*0.04)
    medFiltWin = np.round(medFiltWin_array)     # % around 30 x 30
    
    bgImg =cv2.medianBlur(imgPlane, medFiltWin)
    
    normImg = float(imgPlane)-float(bgImg)
    
    currMean = np.mean(normImg[:])
    currStd = np.std(normImg[:])
    
    normImg = np.multiply((normImg - currMean) , 1/currStd)
    normImg =  np.multiply(normImg,stdTgt) 
    normImg =  normImg + meanTgt
        
    return normImg