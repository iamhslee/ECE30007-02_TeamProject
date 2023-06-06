import os
import shutil
import imghdr
import argparse
import datetime

# Parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="path to dataset")
args = vars(ap.parse_args())

# Set the path to the dataset
DIR = args["path"]

# Step 1: Delete directories with readme.txt
print('\nStep 1: Delete directories with "readme.txt"')
for root, dirs, files in os.walk(DIR):
    if "readme.txt" in files:
        shutil.rmtree(root)
        print("Deleted", root)

# Step 2: Delete unreadable images & weird file names (not following the format: "root*_yymmddhhmmss.jpg")
print("\nStep 2: Delete unreadable images")
for root, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith(".jpg"):
            try:
                imghdr.what(os.path.join(root, file))
            except:
                os.remove(os.path.join(root, file))
                print("Deleted", os.path.join(root, file))

            # Check the format of the file name
            # there should have alphabet, and numbers
            # and the length of the file name should be 18
            if (
                not file.split("_")[0][:-2].isalpha()
                or not file.split("_")[0][-1].isnumeric()
                or not file.split("_")[1].split(".")[0].isnumeric()
                or len(file.split("_")[1].split(".")[0]) != 12
            ):
                os.remove(os.path.join(root, file))
                print("Deleted", os.path.join(root, file))

# Step 3: Rename every ".jpg" files
#         The original image file name format is "root*_yymmddhhmmss.jpg"
#         (e.g. "root1_220923114836.jpg" which means the image was taken at 2022/09/23 11:48:36)
#         The new image file name format is "unixtimestamp.jpg"
#         (e.g. using the previous example, the new file name is "1663901316.jpg")
print('\nStep 3: Rename every ".jpg" files')
for root, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith(".jpg"):
            # Get UNIX Timestamp using original image file name
            unix_time = int(
                datetime.datetime.timestamp(
                    datetime.datetime.strptime(
                        file.split("_")[1].split(".")[0], "%y%m%d%H%M%S"
                    )
                )
            )
            # Get the original image file name
            old_file_name = os.path.join(root, file)
            # Get the new image file name
            new_file_name = os.path.join(root, str(unix_time) + ".jpg")

            # Rename the image file
            os.rename(old_file_name, new_file_name)
            print("Renamed", old_file_name, "to", new_file_name)

# Step 4: Move every single image file to the /train and root/test
#         If original location of image was Dataset/train/~~~, then move it to Dataset/train
#         If original location of image was Dataset/test/~~~, then move it to Dataset/test
print("\nStep 4: Move every single image file")
for root, dirs, files in os.walk(DIR):
    for file in files:
        if file.endswith(".jpg"):
            # Get the original image file name
            old_location = os.path.join(root, file)
            # Get the new image file name
            if "train" in root:
                new_location = os.path.join(DIR, "train")
            elif "test" in root:
                new_location = os.path.join(DIR, "test")
            else:
                print("Error: Invalid path")
                exit()

            new_location = os.path.join(new_location, file)

            # Move the image file
            shutil.move(old_location, new_location)
            print("Moved", old_file_name, "to", new_file_name)

# Step 5: Delete empty directories
print("\nStep 5: Delete empty directories")
for root, dirs, files in os.walk(DIR):
    if len(dirs) == 0 and len(files) == 0:
        shutil.rmtree(root)
        print("Deleted", root)

# Step 6: Sort every image file in /train and /test by filename, then
#         rename it.
#         1. visit every leaf directory in /train and /test
#         2. sort every image file in the leaf directory by filename
#         3. Pick the first image from sorted list and save it to variable called "offset"
#         4. Rename every image file in the leaf directory by subtracting "offset" to its filename
#            To calculate the relative timestamp.
print("\nStep 6: Sort and rename every image file in /train and /test")
for root, dirs, files in os.walk(DIR):
    if len(dirs) == 0:
        # Sort every image file in the leaf directory by filename
        files.sort()

        # Get the offset
        offset = int(files[0].split(".")[0])

        # Rename every image file in the leaf directory by subtracting "offset" to its filename
        for file in files:
            old_file_name = os.path.join(root, file)
            new_file_name = os.path.join(
                root, str(int(file.split(".")[0]) - offset) + ".jpg"
            )
            os.rename(old_file_name, new_file_name)
            print("Renamed", old_file_name, "to", new_file_name)

# Step 7: Create 6 directories at DIR/train and DIR/test
classes = ["0012", "1224", "2436", "3648", "4860", "6072"]

print("\nStep 7: Create directories at /DIR/train and /DIR/test")
for root, dirs, files in os.walk(DIR):
    if "train" in root:
        for class_name in classes:
            os.makedirs(os.path.join(root, class_name))
            print("Created", os.path.join(root, class_name))
    elif "test" in root:
        for class_name in classes:
            os.makedirs(os.path.join(root, class_name))
            print("Created", os.path.join(root, class_name))
    else:
        continue

# Step 8: Move every image file to the corresponding directory
print("\nStep 8: Move every image file to the corresponding directory")
for root, dirs, files in os.walk(DIR):
    if len(dirs) == 0:
        for file in files:
            if file.endswith(".jpg"):
                # Get the image directory
                image_dir = os.path.join

                # Get the image file name
                image_file_name = os.path.join(root, file)

                # Set the class index (0 ~ 5, 12 hours each, filename unit is seconds)
                class_index = int(float(file.split(".")[0]) / 3600.0 / 12.0)

                # Get the new image file name
                new_image_file_name = os.path.join(root, class_name)
                new_image_file_name = os.path.join(new_image_file_name, file)

                # Move the image file
                shutil.move(image_file_name, new_image_file_name)
                print("Moved", image_file_name, "to", new_image_file_name)

# Step 9: Delete empty directories
print("\nStep 9: Delete empty directories")
for root, dirs, files in os.walk(DIR):
    if len(dirs) == 0 and len(files) == 0:
        shutil.rmtree(root)
        print("Deleted", root)
