import numpy as np
import cv2 as cv2
from pywt import swt2 , iswt2

# pierre amir
def findGoodResolutionForWavelet( sizeIn ):
    # Parameters
    maxWavDecom = 2;
    pxToAddC = np.power(2,maxWavDecom) - (sizeIn[1] % np.power(2,maxWavDecom))
    pxToAddR = np.power(2,maxWavDecom) - (sizeIn[0] % np.power(2,maxWavDecom))
    sizeOut =  np.array([sizeIn[0] + pxToAddR, sizeIn[1] + pxToAddC])
    return sizeOut

def preprocessWavelet( imgIn, fovMask ) :
    # % Parameters
    maxWavDecom = 2;
    # %


    
    [imgA,imgH,imgV,imgD] = swt2( imgIn, level = maxWavDecom, wavelet= 'haar' );
    imgRecon = iswt2( np.zeros(imgA[:,:,1].shape),imgH[:,:,1],imgV[:,:,1],imgD[:,:,1], 'haar' )

    imgRecon[imgRecon < 0] = 0
    imgRecon = int( imgRecon )

    imgRecon = imgRecon * int(fovMask);
    imgOut = imgRecon * ( 255 / np.max(imgRecon[:]) )
    return imgOut