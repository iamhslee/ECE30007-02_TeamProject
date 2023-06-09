import os
from datetime import datetime
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="path to the directory")
args = vars(ap.parse_args())

path = args["path"]
classes = ["0012", "1224", "2436", "3648", "4860", "6072", "OVER"]

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
