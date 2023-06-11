import os
import shutil
import PIL.Image as Image
import PIL.ImageFilter as ImageFilter
from datetime import datetime
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="path to the directory")
args = vars(ap.parse_args())

path = args["path"]
classes = ["0012", "1224", "2436", "3648", "4860", "6072", "OVER"]

# Delete every directory which has readme.txt
for root, dirs, files in os.walk(path):
    if len(dirs) == 0:
        if "readme.txt" in files:
            shutil.rmtree(root)

# Rename every file from date string to UNIX timestamp
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".jpg"):
            old_filename = file.split("_")[1].split(".")[0]
            new_filename = int(
                datetime.strptime(old_filename, "%y%m%d%H%M%S").timestamp()
            )
            os.rename(
                os.path.join(root, file),
                os.path.join(root, str(new_filename) + ".jpg"),
            )

# Sort files and rename
for root, dirs, files in os.walk(path):
    if len(dirs) == 0:
        files.sort()
        first_file = int(files[0].split(".")[0])
        for file in files:
            old_filename = int(file.split(".")[0])
            new_filename = old_filename - first_file
            os.rename(
                os.path.join(root, file),
                os.path.join(root, str(new_filename) + ".jpg"),
            )

# Move every files to their parent directory
for root, dirs, files in os.walk(path):
    if len(dirs) == 0:
        for file in files:
            if file.endswith(".jpg"):
                # Check if there any duplicate file
                if os.path.exists(os.path.join(root, "../", file)):
                    new_file_name = int(file.split(".")[0]) + 1
                    os.rename(
                        os.path.join(root, file),
                        os.path.join(root, str(new_file_name) + ".jpg"),
                    )
                shutil.move(os.path.join(root, file), os.path.join(root, "../"))

# Create directory for each class
for root, dirs, files in os.walk(path):
    if root.endswith("test") or root.endswith("train"):
        for c in classes:
            os.mkdir(os.path.join(root, c))

        for file in files:
            if file.endswith(".png"):
                file_name = int(file[:-4])
                idx = 0
                if file_name > 259200:
                    idx = 6
                elif file_name > 216000:
                    idx = 5
                elif file_name > 172800:
                    idx = 4
                elif file_name > 129600:
                    idx = 3
                elif file_name > 86400:
                    idx = 2
                elif file_name > 43200:
                    idx = 1
                else:
                    idx = 0

                # move file to the corresponding folder
                os.rename(
                    os.path.join(root, file), os.path.join(root, classes[idx], file)
                )

# Convert image to grayscale & apply filters
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".jpg"):
            try:
                img = Image.open(os.path.join(root, file)).convert("L")
                # Image pipeline
                img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
                img = img.filter(ImageFilter.FIND_EDGES)
                img = img.point(lambda p: 255 if p > 100 else 0)
                img = img.resize((235, 128))
                img = img.crop((60, 0, 188, 128))
                # End of pipeline
                img.save(os.path.join(root, file[:-4] + ".png"), "PNG")
            except:
                os.remove(os.path.join(root, file))

for root, dirs, files in os.walk(path):
    if len(dirs) == 0:
        if len(files) == 0:
            shutil.rmtree(root)
