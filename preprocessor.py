import os
import shutil
train_file_names=os.listdir("./fisheye_day/images/validation")
label_files=os.listdir("./fisheye_day/labels/validation")

out_file=open("validationData.txt","a")

for f in train_file_names:
	out_file.write("./images/validation/"+f+"\n")
	#f_1=f.split(".")[0]
	#f_labl=f_1+".txt"
	#if f_labl in label_files:
	#	print(f)
	#	print(f_labl)
	#	print("----")
#out_file.close()

#f=open("trainData.txt","r")
#print(f.read())

'''f= open("dev_split.txt","r")
lines=f.read().split("\n")
for line in lines:
	img="./fisheye_day/images/train/"+line+".jpg"
	label="./fisheye_day/labels/train/"+line+".txt"
	shutil.move(img, './fisheye_day/images/validation/')
	shutil.move(label, './fisheye_day/labels/validation/')
	print(line)'''