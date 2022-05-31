
# The Hamilton Eye Institute Macular Edema Dataset

test image processing algorithms for the detection of exudates and diabetic macular edema.

## input image

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)
after reading image we begin in seriese of functions determining  features of image and analisng leassions to extract 

## Running Tests
read file of data to put in the exdetect file

## in class Dmed
reading image
```bash
    #get number of image in file
    def getNumofImgs(self):
        return self.imgNum

    #read each image (.jpg) in file 
    def getImg(self,id):
    #id of image = number of image , then get image name and add it to extention to read it
        if(id < 0 or id>self.imgNum):
            img = []
            raise Exception('Index exceeds dataset size of'+str(self.imgNum))
        else:
            imagename = str(self.data.get(self.idMap[id]-1))+self.imgExt
            imgAddress = os.path.join(self.baseDir+'/'+imagename)
            img = plt.imread(imgAddress)
            return img

    #read each image (.meta) in file 
    def getONloc(self,id):
        onRow = []
        onCol = []
        if(id < 0 or id > self.imgNum):
            raise Exception('Index exceeds dataset size of'+str(self.imgNum))

    #extract patient data from image 
        else:
            name = self.data.get(self.idMap[id]-1)+self.metaExt
            metafile = os.path.join(self.baseDir+"/"+name)

            openMetaFile = open(metafile)
            fmeta = openMetaFile.read()
            openMetaFile.close()
            tokRow = re.search('ONrow\W+([0-9\.]+)', fmeta)
            tokCol = re.search('ONcol\W+([0-9\.]+)', fmeta)
 
            if( tokRow and tokCol ):
                onRow = float(tokRow[1])
                onCol = float(tokCol[1])
            return onRow, onCol   
```
 ## function get lessions 
 
 image is sent to the fun to extract all fetures and plot the otput image

```bash
  def getLesions(rgbImgOrig, showRes, removeON, onY, onX):

```
this function calls all the functis of preprocessing

first resizing and preparing the image
```bash
    height, width, channels = rgbImgOrig.shape #get alriginal dimentions
    origSize = [height, width]
    newSize = [750, round(750*(origSize[1]/origSize[0]))] #preparing new size of image
    newSize = findGoodResolutionForWavelet(newSize)   #new resolution most sutibale for wavlet preprocessing if needed
    imgRGB = cv2.resize(rgbImgOrig, newSize)
    imgG = imgRGB[:, :, 1] #extract the green channel for preprocessing
    # change colour plane to hu , saturation and value (HSV)
    imgHSV = sk.color.rgb2hsv(imgRGB)
    #extract the image value channel
    imgV = imgHSV[:, :, 2]
    imgV8 = imgV * 255
    imgV8 = imgV8.astype(np.int8)
```

```bash
    imgFovMask = getFovMask(imgV8, 1, 30)

    imgFovMask[int(winOnCoordY[0]):int(winOnCoordY[1]),
             int(winOnCoordX[0]):int(winOnCoordX[1])] = 0
 ```
 ## function FovMask
  ```bash
    def getFovMask(gImg,erodeFlag,seSize): 
        lowThresh = 0
    if  seSize==None:
        seSize = 10
    
    histRes = hist(gImg) #extract the white circle in  the eye as it'svalue is zeros 
    
    d = np.diff(histRes) #diffrentat the image and the white circle
    lvlFound = np.where(d >= lowThresh)
    lvlFound=lvlFound[0]
    lvl=lvlFound[0]
    fovMask = np.logical_not(gImg <= lvl) 
#remove the white circcl e using erde function on image 
    if ( erodeFlag > 0):
        se=cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE,ksize=(seSize,seSize))
        fovMask = cv2.erode(np.float32(fovMask),se)
      
        #erode also borders
        fovMask[1:seSize*2,:] = 0
        fovMask[:,1:seSize*2] = 0
        fovMask[-1-seSize*2:-1,:] = 0
        fovMask[:,-1-seSize*2:-1] = 0
``` 
back to lession func
```bash
    # fixed threshold using median Background (with reconstruction)
    kernal_size = round(newSize[0]/30)
    medBg = signal.medfilt2d(imgV8, round(newSize[0]/30))
    # reconstruct bg
    maskImg = imgV8
    maskImg = maskImg
    pxLbl = maskImg < medBg
    maskImg[pxLbl] = medBg[pxLbl]
    medRestored = sk.morphology.reconstruction(medBg, maskImg)
    # subtract, remove fovMask and threshold
    subImg = imgV8 - medRestored
    subImg = subImg * imgFovMask
    subImg[subImg < 0] = 0
    imgThNoOD = subImg.astype(np.int8) > 0
``` 

```bash
     # %--- Calculate edge strength of lesions
    imgKirsch = kirschEdges(imgG)
    img0 = imgG * (imgThNoOD == 0)
    img0recon = sk.morphology.reconstruction(img0, imgG)
    img0Kirsch = kirschEdges(img0recon)
    # % edge strength map
    imgEdgeNoMask = imgKirsch - img0Kirsch
    
    # %---
    # % remove mask and ON (leave vessels)
    imgEdge = imgFovMask * imgEdgeNoMask
    
       
    #  Calculate edge strength for each lesion candidate (Matlab2008)
    lesCandImg = np.zeros_like(imgEdge)
    lblImg = label(imgThNoOD, connectivity=2)
    lesCand = regionprops(lblImg)

    for idxLes in range(0, len(lesCand)):
        pxIdxList = lesCand[idxLes].coords
        pxIdxList=pxIdxList[:,0],pxIdxList[:,1]
        lesCandImg[pxIdxList] = np.sum(imgEdge[pxIdxList]) / len(pxIdxList)

        #  resize back
    lesCandImg = cv2.resize(lesCandImg, origSize,
                            interpolation=cv2.INTER_NEAREST)
```

## kirschEdges fun 
takes image applies splatial filter to detect edges of vesselses to extract it from imageand then Background is what remains 
```bash
    def kirschEdges(imgIn):
    h1 = np.array([[5, - 3, - 3], [5, 0, - 3], [5, - 3, - 3]], dtype=np.float32)/15
    h2 = np.array([[-3, - 3, 5], [- 3, 0, 5], [- 3, - 3, 5]], dtype=np.float32)/15
    h3 = np.array([[-3, - 3, - 3], [5, 0, - 3], [5, 5, - 3]], dtype=np.float32)/15
    h4 = np.array([[-3, 5, 5], [- 3,  0,  5], [- 3, - 3, - 3]],dtype=np.float32)/15
    h5 = np.array([[-3, - 3, - 3], [- 3, 0, - 3], [5,  5, 5]], dtype=np.float32)/15
    h6 = np.array([[5, 5,  5], [- 3, 0, - 3], [- 3, - 3, - 3]],dtype=np.float32)/15
    h7 = np.array([[-3, - 3, - 3], [- 3, 0, 5], [- 3, 5, 5]],dtype=np.float32)/15
    h8 = np.array([[5, 5, - 3], [5,  0, - 3], [- 3, - 3, - 3]], dtype=np.float32)/15
```
 
## output image

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Installation

Install libraries 

```bash
  pip install -r requirments.txt
```
 ## to Run proj

for windows

```bash
  python test.py
```
for linux

```bash
  python3 test.py
```


