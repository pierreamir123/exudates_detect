import os
from Dmed_class import*



DMEDloc = './DMED'
data = Dmed(DMEDloc) # object of Dmed class


print(data.getNumofImgs())
for i in range (1,data.getNumofImgs()):
    rgbImg = data.getImg(i)
    [onY, onX] = data.getONloc(i)



