import os
#import Dmed as getfiles
from Dmed_class import*
# import matplotlib
# import matplotlib.pyplot as plt


DMEDloc = './DMED'
data = Dmed(DMEDloc) # object of Dmed class

# print("locationsss")
# print(DMEDloc)
print(data.getNumofImgs())
for i in range (1,data.getNumofImgs()):
    rgbImg = data.getImg(i)
    #print(rgbImg)
      
    # self.idMap = i    
    # print(self.idMap)


