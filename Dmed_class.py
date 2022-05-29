from ast import Num
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Dmed:
    def __init__(self,baseDir):
        # self.data = data
        # self.origImgNum = realImageNum
        # self.imgNum = currentImgNum
        # self.idMap= Mapid
        self.roiExt = '.jpg.ROI'
        self.imgExt = '.jpg'
        self.metaExt = '.meta'
        self.gndExt = '.GND'
        self.mapGzExt = '.map.gz'
        self.mapExt = '.map'
        self.baseDir = baseDir
        self.data = dict([])
        idxData = 0
        file =  os.listdir(baseDir)
        #print("nice")
        #print(file)
        for file in os.listdir(self.baseDir):
            if file.endswith(self.imgExt):
               #print(os.path.join(self.baseDir, file))
               self.data[idxData],var = os.path.splitext(file)
               idxData = idxData+1
               
        #print(self.data) 
        #print(len(self.data))   
        self.origImgNum = len(self.data)  
        self.imgNum = self.origImgNum 
        #self.idMap = 1:self.imgNum         ##########
        #for i in range (1,self.imgNum+1):
        self.idMap = np.linspace(1,self.imgNum,num=self.imgNum)  
        self.idMap = self.idMap.astype(np.int32)
        #self.idMap = range (1,self.imgNum+1)
        print(self.idMap)
            
    
    # #Dmed function in matlab    
    # def readFile(self,dirIn):
    #     self.baseDir = dirIn
    #     self.data = dict([])
    #     idxData = 0
    #     file =  os.listdir(dirIn)
    #     #print("nice")
    #     #print(file)
    #     for file in os.listdir(self.baseDir):
    #         if file.endswith(self.imgExt):
    #            #print(os.path.join(self.baseDir, file))
    #            self.data[idxData],var = os.path.splitext(file)
    #            idxData = idxData+1
               
    #     #print(self.data) 
    #     #print(len(self.data))   
    #     self.origImgNum = len(self.data)  
    #     self.imgNum = self.origImgNum 
    #     #self.idMap = 1:self.imgNum         ##########
    #     for i in range (1,self.imgNum+1):
    #         self.idMap = i
    #         #print(self.idMap)
            
    def getNumofImgs(self):
            return self.imgNum
        
    def getImg(self,id):
        if(id < 0 or id>self.imgNum):
            img = []
            raise Exception('Index exceeds dataset size of'+str(self.imgNum))
        else:
            imagename = self.data.get(self.idMap[id])+self.imgExt
            imgAddress = os.path.join(self.baseDir, imagename)
            print(imgAddress)
            img = plt.imread(imgAddress)
            
            return img
        
    
               