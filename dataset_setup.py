# AI프로젝트입문 (ECE30007-02)
# Spring, 2023

# Team Project: 미드바르 뿌리 이미지 인식 챌린지
# dataset_setup.py
# - Author: 이현서(ID# 22100600) <hslee@handong.ac.kr>

# This script is for setting up the dataset.

import os
import shutil
import PIL.Image as Image
import argparse
import datetime
import time

# Argument Parser
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="path to dataset")
args = vars(ap.parse_args())

# Set the path to the dataset
DIR = args["path"]

print("Path to dataset:", DIR)

# Step 0: Print directory tree
print("\nStep 0: Print directory tree")
for root, dirs, files in os.walk(DIR):
    level = root.replace(DIR, "").count(os.sep)
    indent = " " * 4 * (level)
    print("{}{}/".format(indent, os.path.basename(root)))
    subindent = " " * 4 * (level + 1)
    for f in files:
        print("{}{}".format(subindent, f))

# Step 1: Delete directories with readme.txt
print('\nStep 1: Delete directories with "readme.txt"')
for root, dirs, files in os.walk(DIR):
    if "readme.txt" in files:
        shutil.rmtree(root)
        print("Deleted", root)

# Step 2: Validate images
print("\nStep 2: Validate images")
for root, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith(".jpg"):
            # Image format validation
            try:
                print("Validated", os.path.join(root, file))
                img = Image.open(os.path.join(root, file))
            except Exception as e:
                print("Exception:", e)
                os.remove(os.path.join(root, file))
                print("Deleted (Format)", os.path.join(root, file))
                continue

            # File name validation
            # Format: "root*_yymmddhhmmss.jpg" (* is 1 digit number)

            # Check the length of the file name (it must be 18 + 4 (extension) = 22)
            if len(file) != 22:
                os.remove(os.path.join(root, file))
                print("Deleted (Name)", os.path.join(root, file))
                continue

            # Check the format of the file name
            # Allow only alphabet, numbers, and underscore
            if (
                not file.split("_")[0][:-2].isalpha()
                or not file.split("_")[0][-1].isnumeric()
                or not file.split("_")[1].split(".")[0].isnumeric()
                or len(file.split("_")[1].split(".")[0]) != 12
            ):
                os.remove(os.path.join(root, file))
                print("Deleted", os.path.join(root, file))
                continue

# Step 3: Rename every dataset images
#        The original image file name format is "root*_yymmddhhmmss.jpg" (* is 1 digit number, yymmddhhmmss is date format which is identical to %y%m%d%H%M%S)
#        Rename the image file name to UNIX Timestamp parse from the original image file name
print("\nStep 3: Rename every dataset images")
for root, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith(".jpg"):
            original_time = file.split("_")[1].split(".")[0]
            date_time = datetime.datetime(
                int("20" + original_time[0:2]),
                int(original_time[2:4]),
                int(original_time[4:6]),
                int(original_time[6:8]),
                int(original_time[8:10]),
                int(original_time[10:12]),
            )
            unix_timestamp = int(time.mktime(date_time.timetuple()))
            os.rename(
                os.path.join(root, file),
                os.path.join(root, str(unix_timestamp) + ".jpg"),
            )
            print(
                "Renamed",
                os.path.join(root, file),
                "to",
                os.path.join(root, str(unix_timestamp) + ".jpg"),
            )

# Step 4: Rename every images in each leaf directory
print("\nStep 4: Rename every images in each leaf directory")
for root, dirs, files in os.walk(DIR):
    if len(dirs) == 0:
        files.sort()
        first_file_name = int(files[0].split(".")[0])
        for file in files:
            other_file_name = int(file.split(".")[0])
            os.rename(
                os.path.join(root, file),
                os.path.join(root, str(other_file_name - first_file_name) + ".jpg"),
            )
            print(
                "Renamed",
                os.path.join(root, file),
                "to",
                os.path.join(root, str(other_file_name - first_file_name) + ".jpg"),
            )

# Step 5: Move every dataset images to the proper directory
print("\nStep 5: Move every dataset images to the proper directory")
for root, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith(".jpg"):
            try:
                shutil.move(os.path.join(root, file), os.path.join(root, "../"))
                print(
                    "Moved",
                    os.path.join(root, file),
                    "to",
                    os.path.join(root, "../"),
                )
            except:
                os.remove(os.path.join(root, file))
                print("Deleted (Duplicate)", os.path.join(root, file))
                continue

# Step 6: Delete empty directories
print("\nStep 6: Delete empty directories")
for root, dirs, files in os.walk(DIR):
    if len(dirs) == 0 and len(files) == 0:
        shutil.rmtree(root)
        print("Deleted", root)

# Step 7: Create subdirectories at /train and /test
classes = [
    "0012",
    "1224",
    "2436",
    "3648",
    "4860",
    "6072",
    "over",
]
print("\nStep 7: Create subdirectories at /train and /test")
for root, dirs, files in os.walk(DIR):
    if root.endswith("/train") or root.endswith("/test"):
        for class_name in classes:
            os.mkdir(os.path.join(root, class_name))
            print("Created", os.path.join(root, class_name))

# Step 8: Move every images to the proper directory
print("\nStep 8: Move every images to the proper directory")
for root, dirs, files in os.walk(DIR):
    if root.endswith("/train") or root.endswith("/test"):
        for file in files:
            if file.endswith(".jpg"):
                class_index = 0
                if int(file.split(".")[0]) >= 0 and int(file.split(".")[0]) < 43200:
                    class_index = 0
                elif (
                    int(file.split(".")[0]) >= 43200 and int(file.split(".")[0]) < 86400
                ):
                    class_index = 1
                elif (
                    int(file.split(".")[0]) >= 86400
                    and int(file.split(".")[0]) < 129600
                ):
                    class_index = 2
                elif (
                    int(file.split(".")[0]) >= 129600
                    and int(file.split(".")[0]) < 172800
                ):
                    class_index = 3
                elif (
                    int(file.split(".")[0]) >= 172800
                    and int(file.split(".")[0]) < 216000
                ):
                    class_index = 4
                elif (
                    int(file.split(".")[0]) >= 216000
                    and int(file.split(".")[0]) < 259200
                ):
                    class_index = 5
                elif int(file.split(".")[0]) >= 259200:
                    class_index = 6
                else:
                    os.remove(os.path.join(root, file))
                    print("Deleted", os.path.join(root, file))
                    continue

                shutil.move(
                    os.path.join(root, file),
                    os.path.join(root, classes[class_index], file),
                )
                print(
                    "Moved",
                    os.path.join(root, file),
                    "to",
                    os.path.join(root, classes[class_index], file),
                )
