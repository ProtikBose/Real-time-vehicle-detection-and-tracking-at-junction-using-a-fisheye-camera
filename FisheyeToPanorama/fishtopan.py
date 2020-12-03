import cv2
import numpy as np
import time

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

# build the mapping
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

# do the unwarping 
def unwarp(img,xmap,ymap):
    output = cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    
    return output

# initialization
vals = []
last = (0,0)

# reading image
img = cv2.imread("frame_cnr_6_000229.jpg")
print(img.shape)

# center of the picture    
Cx = int(img.shape[0]/2)
Cy = int(img.shape[1]/2)
# Inner circle radius
R1x = int(img.shape[0]/2)+int(img.shape[0]/4)
# R1 = R1x-Cx
R1 = 0

# outer circle radius
R2x = int(img.shape[0])
R2 = R2x-Cx

# our input and output image sizes
# Wd = int(2.0*((R2+R1)/2)*np.pi)
Ws = img.shape[1]
Hs = img.shape[0]
Wd = int(2*np.pi*R2)
Hd = (R2-R1)


# build the pixel map, this could be sped up
print("BUILDING MAP!")
xmap,ymap = buildMap(Ws,Hs,Wd,Hd,R1,R2,Cx,Cy)
print("MAP DONE!")

result = unwarp(img,xmap,ymap)
#cv2.imshow("undistorted",result)
#cv2.waitKey(0)
result = rotate_bound(result,180)
cv2.imwrite("1_pano.jpg",result)

print(xmap.shape)
print(xmap)

    
