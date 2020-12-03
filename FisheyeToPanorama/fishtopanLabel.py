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

        MidX.append(midx*1280)
        MidY.append(midy*1280)
        TopX.append(topx*1280)
        TopY.append(topy*1280)
        Width.append(width)
        Height.append(height)

    return MidX, MidY, TopX, TopY, Width, Height

def buildMap2(arrayX, arrayY, Wd, Hd, Cx, Cy):
    newArrayX = []
    newArrayY = []

    for i in range(len(arrayX)):
        x = arrayX[i]
        y = arrayY[i]

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

        newArrayX.append(Xd)
        newArrayY.append(Yd)
    return newArrayX, newArrayY

def rotate_bound(arrayX, arrayY, Wd, Hd, Cx, Cy):
    h = Hd
    w = Wd
    M = cv2.getRotationMatrix2D((Cx, Cy), -180, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - Cx
    M[1, 2] += (nH / 2) - Cy

    newArrayX = []
    newArrayY = []

    for i in range(len(arrayX)):
        newX = M[0,0]*arrayX[i]*Wd + M[0,1]*arrayY[i]*Hd + M[0,2]
        newY = M[1,0]*arrayX[i]*Wd + M[1,1]*arrayY[i]*Hd + M[1,2]
        newArrayX.append(newX/Wd)
        newArrayY.append(newY/Hd)

    #return newArrayX, newArrayY
    arrayX = np.reshape(arrayX, (len(arrayX), -1))
    arrayY = np.reshape(arrayY, (len(arrayY), -1))
    array = np.concatenate((arrayX, arrayY), axis=1)
    print(array.shape)
    print(array)
    return cv2.warpAffine(array, M, array.shape)


MidX, MidY, TopX, TopY, Width, Height = readFromLabel("frame_cnr_6_000229.txt")
print(MidX)
print(len(MidX))
newMidX, newMidY = buildMap2(MidX, MidY, 4021, 640, 1280/2, 1280/2)
newTopX, newTopY = buildMap2(TopX, TopY, 4021, 640, 1280/2, 1280/2)
print("After BuildMap: ")
print(newMidX)
print(newMidY)
#newMidX, newMidY = rotate_bound(newMidX, newMidY, 4021, 640, 4021/2, 640/2)
#newTopX, newTopY = rotate_bound(newTopX, newTopY, 4021, 640, 4021/2, 640/2)
newMid = rotate_bound(newMidX, newMidY, 4021, 640, 4021/2, 640/2)
print("After RotateBound: ")
#print(newMidX)
#print(newMidY)
print(newMid)

img = cv2.imread("1_pano.jpg")
plt.figure()
plt.imshow(img)
for i in range(len(newMidX)):
    circMid = Circle((newMidX[i]*4021, newMidY[i]*640), 10, color='red')
    circTop = Circle((newTopX[i]*4021, newTopY[i]*640), 10, color='blue')
    rect = Rectangle((newTopX[i]*4021, newTopY[i]*640), Width[i]*(4021), Height[i]*(640), fill=False, color='green')
    plt.axes().add_patch(circMid)
    plt.axes().add_patch(circTop)
    plt.axes().add_patch(rect)
plt.show()
        