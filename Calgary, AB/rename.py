import os

folder_path = "ERA5Land" # path to the folder containing the files
for filename in os.listdir(folder_path):
    # if filename.endswith(".nc"):
    new_filename = filename[:4] + filename[5:]
    os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
