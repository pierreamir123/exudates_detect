import os
from Dmed_class import*
from exdetect_test_func import exDetect


DMEDloc = './DMED'
data = Dmed(DMEDloc) # object of Dmed class


# print(data.getNumofImgs())
for i in range (0,data.getNumofImgs()):
    rgbImg = data.getImg(i)
    [onYY, onXX] = data.getONloc(i)
    exDetect(rgbImgOrig=rgbImg , onX=onXX, onY=onYY, removeON=1)


