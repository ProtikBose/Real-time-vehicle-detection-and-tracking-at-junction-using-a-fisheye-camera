import math
import cv2
import os


def rotate_around_point_lowperf(point, radians, origin=(0, 0)):
    x, y = point
    ox, oy = origin

    qx = ox + -math.cos(radians) * (-x + ox) + math.sin(radians) * (-y + oy)
    qy = oy + -math.sin(radians) * (-x + ox) + -math.cos(radians) * (-y + oy)

    return qx, qy

def rotate_lengths(length_tuple, radians):
    bx, by = length_tuple
    # x= bx * math.cos(radians) + by * math.sin(radians)
    # y= by * math.cos(radians) - bx * math.sin(radians)
    x= math.sqrt((bx * math.cos(radians))**2 + (by * math.sin(abs(radians)))**2)
    y= math.sqrt((by * math.cos(radians))**2 + (bx * math.sin(abs(radians)))**2)
    #print(x,y)
    return x,y

def read_and_write(input_folder,image_file,label_folder,out_folder):
    print(image_file)
    image=cv2.imread(input_folder+"/"+image_file)
    print(image.shape[0])
    print(image.shape[1])


    file_name_parts=image_file.split(".")[0]
    fn_parts2=file_name_parts.split("_")


    #actual_image=fn_parts2[0]+fn_parts2[1]+fn_parts2[2]+".jpg"

    #actual_image_labels=label_folder+"/"+fn_parts2[0]+"_"+fn_parts2[1]+"_"+fn_parts2[2]+".txt"
    actual_image_labels=""
    for i in range(len(fn_parts2)-1):
        actual_image_labels=actual_image_labels+fn_parts2[i]
        if i != len(fn_parts2)-2:
            actual_image_labels=actual_image_labels+"_"


    actual_image_labels=label_folder+"/"+actual_image_labels+".txt"

    inf=open(actual_image_labels,"r")
    data=inf.read().split("\n")



    out_file=out_folder+"/"+image_file.split(".")[0]+".txt"
    outf=open(out_file,"w+")
    for d in range(len(data)-1):
        vals=data[d].split(" ")
        # print(len(vals))
        cx=float(vals[1])*image.shape[0]
        cy=float(vals[2])*image.shape[1]
        bx=float(vals[3])
        by=float(vals[4])

        
        angle=float(fn_parts2[3])
        # print(angle)
        theta=math.radians(angle)
        origin=(image.shape[0]/2,image.shape[1]/2)

        point1=(int(cx),int(cy))
        newx,newy=rotate_around_point_lowperf(point1,theta,origin)
        newx_norm=newx/image.shape[0]
        newy_norm=newy/image.shape[1]

        point2=(bx,by)
        x_len,y_len=rotate_lengths(point2,theta)


        str_out="0 "+str(newx_norm)+" "+str(newy_norm)+" "+str(x_len)+" "+str(y_len)+"\n"
        outf.write(str_out)





def _main():
    #theta = math.radians(90)
    #point = (-11, 5)

    #print(rotate_around_point_lowperf(point, theta))
    img_files=os.listdir("Rotated")
    for f in img_files:
        read_and_write("Rotated",f,"fisheye_day/labels/train","Rotated_labels")


if __name__ == '__main__':
    _main()