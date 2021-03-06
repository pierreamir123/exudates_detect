from ast import Num
from cmath import inf
import os
import re
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
        # print('id')
        # print(self.idMap)
            
    
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
            # print('data')
            # print(self.idMap[id])
            #print(self.data)
            #print(self.data.get(self.idMap[id]))
            imagename = str(self.data.get(self.idMap[id]-1))+self.imgExt
            imgAddress = os.path.join(self.baseDir+'/'+imagename)
            img = plt.imread(imgAddress)
            
            return img
    
    def getONloc(self,id):
        onRow = []
        onCol = []
        if(id < 0 or id > self.imgNum):
            raise Exception('Index exceeds dataset size of'+str(self.imgNum))
        else:
            # print('num')
            # print(self.imgNum)
            name = self.data.get(self.idMap[id]-1)+self.metaExt
            metafile = os.path.join(self.baseDir+"/"+name)

            openMetaFile = open(metafile)
            fmeta = openMetaFile.read()
            # print('meta')
            # print(fmeta)
 
            openMetaFile.close()
            

            tokRow = re.search('ONrow\W+([0-9\.]+)', fmeta)
            tokCol = re.search('ONcol\W+([0-9\.]+)', fmeta)
 
            if( tokRow and tokCol ):
                
                onRow = float(tokRow[1])
                onCol = float(tokCol[1])
                # print(onRow)
                # print(onCol)
            return onRow, onCol   

            

        
        
    
               