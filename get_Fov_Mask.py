
from gettext import find
from cv2 import *
import cv2 as cv2
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import skimage as sk

# mai radwan


def hist(GrayScaled):
        r=[]
        im=GrayScaled
        im=np.asarray(im)
        im=np.round(im)
        im=im.astype(int)
        h = [0]*256  
        for x in range(im.shape[0]):        
            for y in range(im.shape[1]):            
                i = round(im[x,y])   
                #specfic intensity
                if i<=256:
                    h[i] = h[i]+1     #had 1 of a specfic intensity then add one and repeat
                else:
                    pass
        for i in range (len(h)):
            r.append(i)
        newh=np.asanyarray(h)
        normalizedH=newh/(im.shape[0]*im.shape[1])
       
    
        return h
def getFovMask(gImg,erodeFlag,seSize): 
    #GETFOVMASK get a binary image of the Field of View mask
    # gImg: green challe uint8 image
    # erodeFlag: if set it will erode the mask
    #Param
    lowThresh = 0
    if  seSize==None:
        seSize = 10
    
    histRes = hist(gImg)
    
    d = np.diff(histRes)
    lvlFound = np.where(d >= lowThresh)
    lvlFound=lvlFound[0]
    lvl=lvlFound[0]
    fovMask = np.logical_not(gImg <= lvl) 
    if ( erodeFlag > 0):
        se=cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE,ksize=(seSize,seSize))
        fovMask = cv2.erode(np.float32(fovMask),se)
      
        #erode also borders
        fovMask[1:seSize*2,:] = 0
        fovMask[:,1:seSize*2] = 0
        fovMask[-1-seSize*2:-1,:] = 0
        fovMask[:,-1-seSize*2:-1] = 0
       
    return fovMask