import numpy as np
from cv2 import *
import cv2 as cv2


def kirschEdges(imgIn):

    # % Kirsch's Templates
    h1 = np.array([[5, - 3, - 3], [5, 0, - 3], [5, - 3, - 3]],
                  dtype=np.float32)/15
    h2 = np.array([[-3, - 3, 5], [- 3, 0, 5], [- 3, - 3, 5]],
                  dtype=np.float32)/15
    h3 = np.array([[-3, - 3, - 3], [5, 0, - 3], [5, 5, - 3]],
                  dtype=np.float32)/15
    h4 = np.array([[-3, 5, 5], [- 3,  0,  5], [- 3, - 3, - 3]],
                  dtype=np.float32)/15
    h5 = np.array([[-3, - 3, - 3], [- 3, 0, - 3],
                  [5,  5, 5]], dtype=np.float32)/15
    h6 = np.array([[5, 5,  5], [- 3, 0, - 3], [- 3, - 3, - 3]],
                  dtype=np.float32)/15
    h7 = np.array([[-3, - 3, - 3], [- 3, 0, 5], [- 3, 5, 5]],
                  dtype=np.float32)/15
    h8 = np.array([[5, 5, - 3], [5,  0, - 3], [- 3, - 3, - 3]],
                  dtype=np.float32)/15

    # % Spatial Filtering by Kirsch's Templates
    t1 = cv2.filter2D(imgIn, -1, h1)
    t2 = cv2.filter2D(imgIn, -1, h2,)
    t3 = cv2.filter2D(imgIn, -1, h3)
    t4 = cv2.filter2D(imgIn, -1, h4)
    t5 = cv2.filter2D(imgIn, -1, h5)
    t6 = cv2.filter2D(imgIn, -1, h6)
    t7 = cv2.filter2D(imgIn, -1, h7)
    t8 = cv2.filter2D(imgIn, -1, h8)

    # % Find the maximum edges value
    imgOut = np.max(t1, t2)
    imgOut = np.max(imgOut, t3)
    imgOut = np.max(imgOut, t4)
    imgOut = np.max(imgOut, t5)
    imgOut = np.max(imgOut, t6)
    imgOut = np.max(imgOut, t7)
    imgOut = np.max(imgOut, t8)

    return imgOut
