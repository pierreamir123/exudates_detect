import os
from Dmed_class import*



DMEDloc = './DMED'
data = Dmed(DMEDloc) # object of Dmed class


# print(data.getNumofImgs())
for i in range (0,data.getNumofImgs()):
    rgbImg = data.getImg(i)
    [onY, onX] = data.getONloc(i)



