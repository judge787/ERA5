import os

# create a list of directory names from 1981 to 1999
# dir_names = [str(year) for year in range(1981, 2000)]
# dir_names = 1990

# # loop through each directory
# for dir_name in dir_names:
#     files = os.listdir(dir_name)

#     # create a list of all the file names in the directory, sorted alphabetically
#     file_names = sorted([os.path.join(dir_name, file_name) for file_name in files])

#     # loop through the list and delete every odd-indexed file
#     for i in range(0, len(file_names), 2):
#         os.remove(file_names[i])

import os

dir_name = "EPW Files/1999" # replace with your directory name
files = os.listdir(dir_name)

# create a list of all the file names in the directory, sorted alphabetically
file_names = sorted([os.path.join(dir_name, file_name) for file_name in files])

# loop through the list and delete every odd-indexed file
for i in range(0, len(file_names), 2):
    os.remove(file_names[i])
