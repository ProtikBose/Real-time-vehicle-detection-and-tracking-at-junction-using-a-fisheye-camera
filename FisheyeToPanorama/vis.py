import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cv2

def plotBoundingBox(imgFile, label):

    img = cv2.imread(imgFile)
    plt.figure()
    plt.imshow(img)
    #Rectangle(topleft_x, topleft_y, width, height)
    f = open(label, 'r')
    allboxes = f.readlines()
    f.close()

    for box in allboxes:
        segs = box.split(' ')
        width = float(segs[3])
        height = float(segs[4])
        topx = float(segs[1]) - width/2
        topy = float(segs[2]) - height/2

        rect = Rectangle(( topx*1280, topy*1280), width*1280, height*1280, fill=False, color='red')
        plt.axes().add_patch(rect)
    plt.show()

# D:\L-4,T-2\IEEE Vip Cup 2020\fisheye-day-30062020\fisheye-day-30062020\images\train\frame_cnr_6_000229.jpg
if __name__=='__main__':
    plotBoundingBox('frame_cnr_6_000229.jpg', 'frame_cnr_6_000229.txt')