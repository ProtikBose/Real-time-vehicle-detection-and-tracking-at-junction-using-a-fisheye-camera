import cv2
import numpy as np
from math import *
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

def readFromLabel(labelFile):
    f = open(labelFile, 'r')
    allboxes = f.readlines()
    f.close()
    MidX = []
    MidY = []
    TopX = []
    TopY = []
    BottomX = []
    BottomY = []
    Width = []
    Height = []

    for box in allboxes:
        segs = box.split(' ')
        midx = float(segs[1])
        midy = float(segs[2])
        width = float(segs[3])
        height = float(segs[4])
        topx = midx - width/2
        topy = midy - height/2
        bottomx = midx + width/2
        bottomy = midy + height/2


        MidX.append(midx*1280)
        MidY.append(midy*1280)
        TopX.append(topx*1280)
        TopY.append(topy*1280)
        BottomX.append(bottomx*1280)
        BottomY.append(bottomy*1280)
        Width.append(width)
        Height.append(height)

    return MidX, MidY, TopX, TopY, BottomX, BottomY, Width, Height

def buildMap(Ws,Hs,Wd,Hd,R1,R2,Cx,Cy):
    map_x = np.zeros((Hd,Wd),np.float32)
    map_y = np.zeros((Hd,Wd),np.float32)
    for y in range(0,int(Hd-1)):
        for x in range(0,int(Wd-1)):
            r = float(y)/float(Hd)*(R2-R1) + R1
            theta = (float(x)/float(Wd))*2.0*np.pi
            xS = Cx+r*np.sin(theta)
            yS = Cy+r*np.cos(theta)
            map_x.itemset((y,x),int(xS))
            map_y.itemset((y,x),int(yS))
        
    return map_x, map_y

def buildMap2(Ws,Hs,Wd,Hd,R1,R2,Cx,Cy):
    map_x = np.zeros((Hs,Ws),np.float32)
    map_y = np.zeros((Hs,Ws),np.float32)
    for y in range(0,int(Hs-1)):
        for x in range(0,int(Ws-1)):
            r = np.sqrt((x-Cx)**2 + (y-Cy)**2)

            if (x<Cx) and (y>Cy):
                theta = atan((x-Cx)/(y-Cy)) + np.pi
            elif (x<Cx) and (y<Cy):
                theta = abs(atan((x-Cx)/(y-Cy))) + np.pi
            elif (x>Cx) and (y>Cy):
                theta = abs(atan((x-Cx)/(y-Cy)))
            elif (x>Cx) and (y<Cy):
                theta = atan((x-Cx)/(y-Cy)) + np.pi*2
            elif y==Cy:
                theta = np.pi/2
            elif x==Cx:
                if(y>Cy):
                    theta = acos((y-Cy)/r) + np.pi
                else:
                    theta = acos((y-Cy)/r) + np.pi*2
            else:
                theta = atan((x-Cx)/(y-Cy))
            
            theta += np.pi/2
            theta = theta % (np.pi*2)
            #theta = theta % ((359*np.pi)/180.00)

            Xd = (((theta)/(2*np.pi))*Wd)
            if (Xd<=Wd/4):
                Xd = Wd/4 - Xd
            elif (Xd>Wd/4) and (Xd<=Wd/2):
                Xd = Wd/2 - Xd + Wd/4
            elif (Xd>Wd/2) and (Xd<=Wd*0.75):
                Xd = Wd*0.75 - Xd + Wd/2
            elif (Xd>Wd*0.75) and (Xd<=Wd):
                Xd = Wd - Xd + Wd*0.75
            
            Yd = Hd-1-r
            
            map_x.itemset((y,x), int(Xd))
            map_y.itemset((y,x), int(Yd))
    
    return map_x, map_y

def unwarp(img,xmap,ymap):
    output = cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    
    return output

def arrayConcat(arrayX, arrayY):
    arrayX = np.reshape(arrayX, (len(arrayX), -1))
    arrayY = np.reshape(arrayY, (len(arrayY), -1))
    array = np.concatenate((arrayX, arrayY), axis=1)

    return array

def convertionByMap(arrayX, arrayY, mapX, mapY):
    newArrayX = []
    newArrayY = []

    for i in range(len(arrayX)):
        x = int(arrayX[i])
        y = int(arrayY[i])

        newArrayX.append(mapX[y, x])
        newArrayY.append(mapY[y, x])

    return newArrayX, newArrayY

def rotate_bound(array, w, h, angle):
    
    (cX, cY) = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    newM = cv2.invertAffineTransform(M)

    newArray = np.zeros((array.shape[0], array.shape[1]))

    for i in range(len(array[:, 0])):
        newArray[i, 0] = newM[0,0]*array[i, 0] + newM[0,1]*array[i, 1] + newM[0,2]
        newArray[i, 1] = newM[1,0]*array[i, 0] + newM[1,1]*array[i, 1] + newM[1,2]
        
    return newArray
    #return cv2.warpAffine(array, M, array.shape, (nW, nH))

def rotate_bound2(array, Wd, Hd):
    Cx = Wd // 2
    Cy = Hd // 2
    for i in range(len(array)):
        if (array[i]<Cx):
            array[i] = array[i] + Cx
        else:
            array[i] = array[i] - Cx
    
    return array

MidX, MidY, TopX, TopY, BottomX, BottomY, Width, Height = readFromLabel("frame_cnr_6_000229.txt")


Ws = Hs = 1280
R2 = int(Ws/2)
R1 = 0
Wd =  int(2*np.pi*R2)
Hd = R2 - R1
Cx = Cy = int(Ws/2)

xmap,ymap = buildMap2(Ws,Hs,Wd,Hd,R1,R2,Cx,Cy)
print(xmap)
print(xmap.shape)
print(ymap)

#result = unwarp(MidArray, xmap, ymap)
#print(result)
#print(result.shape)
print(MidX, MidY)
newMidX, newMidY = convertionByMap(MidX, MidY, xmap, ymap)
print(newMidX, newMidY)
newMidX = rotate_bound2(newMidX, Wd, Hd)

newTopX, newTopY = convertionByMap(TopX, TopY, xmap, ymap)
newTopX = rotate_bound2(newTopX, Wd, Hd)

newBottomX, newBottomY = convertionByMap(BottomX, BottomY, xmap, ymap)
newBottomX = rotate_bound2(newBottomX, Wd, Hd)



img = cv2.imread("1_pano.jpg")
plt.figure()
plt.imshow(img)
for i in range(len(newMidX)):
    circMid = Circle((newMidX[i], newMidY[i]), 10, color='red')
    circTop = Circle((newTopX[i], newTopY[i]), 10, color='blue')
    rect = Rectangle((newTopX[i], newTopY[i]), newBottomX[i]-newTopX[i], newBottomY[i]-newTopY[i], fill=False, color='green')
    plt.axes().add_patch(circMid)
    plt.axes().add_patch(circTop)
    plt.axes().add_patch(rect)
    Width[i] = newBottomX[i]-newTopX[i]
    Height[i] = newBottomY[i]-newTopY[i]

plt.show()

newTopX = np.reshape(newTopX, (len(newTopX), -1))
newTopY = np.reshape(newTopY, (len(newTopY), -1))
Width = np.reshape(Width, (len(Width), -1))
Height = np.reshape(Height, (len(Height), -1))
Zero = np.zeros((newTopX.shape[0], 1))
FinalArray = np.concatenate((Zero, newTopX, newTopY, Width, Height), axis=1)
print(FinalArray)
np.savetxt('frame_cnr_6_000229_PANO.txt', FinalArray, fmt='%.6f')

