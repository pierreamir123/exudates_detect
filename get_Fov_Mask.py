
from gettext import find
from cv2 import *
import cv2 as cv2
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import skimage as sk

# mai radwan


def getFovMask(gImg, erodeFlag=0, seSize=10):
    lowThresh = 0
    histRes = np.histogram(gImg,range=(0,255))
    d = np.diff(histRes[0])
    lvlFound =np.argmax(d >= lowThresh)
    fovMask = ~(gImg <= lvlFound)
    print("fovMask", fovMask)
    if(erodeFlag > 0):
        se =  sk.morphology.disk(seSize)
        fovMask = sk.morphology.binary_erosion(fovMask, se)
        fovMask[0: seSize*2, :] = 0
        fovMask[:, 0: seSize*2] = 0
        fovMask[len(gImg)-seSize*2: len(gImg), :] = 0
        fovMask[:, len(gImg)-seSize*2: len(gImg)] = 0
    return fovMask
