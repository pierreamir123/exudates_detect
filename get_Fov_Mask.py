
from gettext import find
from cv2 import *
import cv2 as cv2
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

# mai radwan


def getFovMask(gImg, erodeFlag, seSize, num_arg):
    lowThresh = 0
    if(num_arg < 3):
        seSize = 10

    histRes = plt.hist(gImg[:], bins=range(0, 1, 255))
    d = np.diff(histRes)

    lvlFound = find(d >= lowThresh, 1, 'first')

    fovMask = not(gImg <= lvlFound)

    if(num_arg > 1 and erodeFlag > 0):
        se = line('disk', seSize)
        fovMask = cv2.erode(fovMask, se)

    # %erode also borders
    fovMask[0: seSize*2, :] = 0
    fovMask[:, 0: seSize*2] = 0
    fovMask[len(gImg)-seSize*2: len(gImg), :] = 0
    fovMask[:, len(gImg)-seSize*2: len(gImg)] = 0

    return fovMask
