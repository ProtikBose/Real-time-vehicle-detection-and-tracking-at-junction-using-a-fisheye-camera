import cv2
import numpy as np
import time
from math import *

# building the map
def buildMap(Ws,Hs,Wd,Hd,R1,R2,Cx,Cy):
    map_x = np.zeros((Hs,Ws),np.float32)
    map_y = np.zeros((Hs,Ws),np.float32)
    for y in range(0,int(Hs-1)):
        for x in range(0,int(Ws-1)):
            if y==Cy:
                theta = np.pi/2
            else:
                theta = (atan((x-Cx)/(y-Cy)))

            if x==Cx:
                r = 0
            elif theta==0:
                r = float(y-Cy) / np.cos(theta)
            else:
                r = float(x-Cx) / np.sin(theta)
            r = np.sqrt((x-Cx)**2 + (y-Cy)**2)
            Xd = (theta*Wd) / (2*np.pi)
            Yd = r - R1
            
            map_x.itemset((y,x), int(Xd))
            map_y.itemset((y,x), int(Yd))
    
    return map_x, map_y

count1 = count2 = count3 = count4 = 0
def countTheta(theta):
    if (theta>0) and (theta<np.pi/2):
        count1 += 1
    elif (theta>np.pi/2) and (theta<np.pi):
        count2 += 1
    elif (theta>np.pi) and (theta<(np.pi*(3/2))):
        count3 += 1
    elif (theta>np.pi*1.5) and (theta<np.pi*2):
        count4 += 1

    return count1, count2, count3, count4

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

# do the unwarping 
def unwarp(img,xmap,ymap):
    output = cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    
    return output

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

img = cv2.imread("1_pano.jpg")
print(img.shape)

# Cx=Cy=1024/2
Wd = int(img.shape[1])
Hd = int(img.shape[0])
# R2 = ((Wd/np.pi)+Hd)/2
# R1 = ((Wd/np.pi)-Hd)/2
R2 = Hd
R1 = 0

Ws=Hs=R2*2
Cx=Cy=Ws/2

print("BUILDING MAP!")
xmap,ymap = buildMap2(Ws,Hs,Wd,Hd,R1,R2,Cx,Cy)
print("MAP DONE!")
#print(ymap)

result = unwarp(img,xmap,ymap)
cv2.imshow("distorted",result)
print(result.shape)

result = rotate_bound(result,180)
print("Result:")
print(result.shape)
print(result)
cv2.imwrite("1_fish.jpg",result)
