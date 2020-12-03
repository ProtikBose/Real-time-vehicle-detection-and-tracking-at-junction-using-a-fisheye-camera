import os
import shutil

def copy_labels(image_folder, label_folder, out_folder):
	img_files=os.listdir(image_folder)
	for imgfile in img_files:
		parts=imgfile.split("_Brightness")
		label_file=label_folder+"/"+parts[0]+".txt"
		copy_file=out_folder+"/"+imgfile.split(".j")[0]+".txt"
		shutil.copy(label_file,copy_file)

def main():
    image_folder="Brightness"
    label_folder="fisheye_day/labels/train"
    out_folder="Brightness_labels"
    copy_labels(image_folder, label_folder, out_folder)

if __name__ == "__main__":
    main()

