# import os
# import zipfile

# def unzip_files_in_directory(directory):
#     for file_name in os.listdir(directory):
#         if file_name.endswith('.zip') and not file_name.startswith('._'):
#             file_path = os.path.join(directory, file_name)
#             try:
#                 with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                     # Extract the contents into the same directory
#                     zip_ref.extractall(directory)

#                     # Rename the extracted file to match the ZIP file name
#                     extracted_file_name = os.path.splitext(file_name)[0] + ".nc"
#                     extracted_file_path = os.path.join(directory, extracted_file_name)
#                     os.rename(os.path.join(directory, os.listdir(directory)[0]), extracted_file_path)

#                 print(f"Unzipped file: {file_name}")

#                 # Delete the ZIP file
#                 os.remove(file_path)
#                 print(f"Deleted file: {file_name}")
#             except zipfile.BadZipFile:
#                 print(f"Skipping file: {file_name} (not a valid ZIP file)")

# # Usage example
# directory_path = './ERA5Land'  # Specify the path to your directory
# unzip_files_in_directory(directory_path)


# import os
# import zipfile

# def unzip_files_in_directory(directory):
#     for file_name in os.listdir(directory):
#         if file_name.endswith('.zip') and not file_name.startswith('._'):
#             file_path = os.path.join(directory, file_name)
#             try:
#                 with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                     # Extract the contents into the same directory
#                     zip_ref.extractall(directory)

#                     # Rename the extracted file to match the ZIP file name
#                     extracted_file_name = os.path.splitext(file_name)[0] + ".nc"
#                     extracted_file_path = os.path.join(directory, extracted_file_name)

#                     # Find the extracted file and rename it
#                     for extracted_file in os.listdir(directory):
#                         if extracted_file.endswith('.nc'):
#                             os.rename(os.path.join(directory, extracted_file), extracted_file_path)
#                             break

#                 print(f"Unzipped file: {file_name}")

#                 # Delete the ZIP file
#                 os.remove(file_path)
#                 print(f"Deleted file: {file_name}")
#             except zipfile.BadZipFile:
#                 print(f"Skipping file: {file_name} (not a valid ZIP file)")






# import os
# import zipfile

# def unzip_files_in_directory(directory):
#     for file_name in os.listdir(directory):
#         if file_name.endswith('.zip') and not file_name.startswith('._'):
#             file_path = os.path.join(directory, file_name)
#             try:
#                 with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                     # Extract the contents into the same directory
#                     zip_ref.extractall(directory)

#                     # Rename the extracted file to match the ZIP file name
#                     extracted_file_name = os.path.splitext(file_name)[0] + ".nc"
#                     extracted_file_path = os.path.join(directory, extracted_file_name)
#                     os.rename(os.path.join(directory, os.listdir(directory)[0]), extracted_file_path)

#                 print(f"Unzipped file: {file_name}")

#                 # Delete the ZIP file
#                 # os.remove(file_path)
#                 # print(f"Deleted file: {file_name}")
#             except zipfile.BadZipFile:
#                 print(f"Skipping file: {file_name} (not a valid ZIP file)")

# # Usage example
# directory_path = 'ERA5Land'  # Specify the path to your directory
# unzip_files_in_directory(directory_path)


# import os
# import shutil
# import zipfile

# def unzip_files_in_directory(directory_path):
#     for root, dirs, files in os.walk(directory_path):
#         for file in files:
#             if file.endswith(".zip"):
#                 file_path = os.path.join(root, file)
#                 print("Unzipping file:", file)
#                 with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                     zip_ref.extractall(root)
#                 new_file_name = file.replace('.zip', '')
#                 new_file_path = os.path.join(root, new_file_name)
#                 os.rename(file_path, new_file_path)
#                 print("Renamed file:", new_file_name)
#                 if os.path.exists(new_file_path):
#                     os.remove(new_file_path)
#                     print("Deleted file:", new_file_name)

# directory_path = './ERA5Land'
# unzip_files_in_directory(directory_path)






# import os
# import zipfile

# def unzip_files_in_directory(directory):
#     count = 0
#     for file_name in os.listdir(directory):
#         if file_name.endswith('.zip') and not file_name.startswith('._'):
#             file_path = os.path.join(directory, file_name)
#             try:
#                 with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                     # Extract the contents into the same directory
#                     zip_ref.extractall(directory)

#                 # Delete the ZIP file
#                 os.remove(file_path)

#                 # Rename the extracted file to match the ZIP file name
#                 extracted_file_name = os.path.splitext(file_name)[0] + ".nc"
#                 extracted_file_path = os.path.join(directory, extracted_file_name)

#                 # Find the extracted file and rename it
#                 extracted_files = [f for f in os.listdir(directory) if f.endswith('.nc')]
#                 if len(extracted_files) > 0:
#                     count += 1
#                     extracted_file = extracted_files[0]
#                     extracted_file_old_path = os.path.join(directory, extracted_file)
#                     os.rename(extracted_file_old_path, extracted_file_path)
#                     print(f"Renamed file: {extracted_file} to {extracted_file_name}")
#                     print(f"Unzipped and renamed file: {file_name}")

#                 else:
#                     print(f"No extracted file found for: {file_name}")

#             except zipfile.BadZipFile:
#                 print(f"Skipping file: {file_name} (not a valid ZIP file)")
#             except FileNotFoundError:
#                 print(f"File not found: {file_path}")
#     print(f"Total files unzipped and renamed: {count}")  # Print total count of files unzipped and renamed

# # Usage example
# directory_path = 'ERA5Land'  # Specify the path to your directory
# unzip_files_in_directory(directory_path)



import os
import zipfile

def unzip_files_in_directory(directory):
    count = 0
    for file_name in os.listdir(directory):
        if file_name.endswith('.zip') and not file_name.startswith('._'):
            file_path = os.path.join(directory, file_name)
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    # Extract the contents into the same directory
                    zip_ref.extractall(directory)

                # Rename the extracted file to match the ZIP file name
                extracted_file_name = os.path.splitext(file_name)[0] + ".nc"
                extracted_file_path = os.path.join(directory, extracted_file_name)

                # Find the extracted file and rename it
                extracted_files = [f for f in os.listdir(directory) if f.endswith('.nc')]
                if len(extracted_files) > 0:
                    count += 1
                    extracted_file = extracted_files[0]
                    extracted_file_old_path = os.path.join(directory, extracted_file)
                    os.rename(extracted_file_old_path, extracted_file_path)
                    print(f"Renamed file: {extracted_file} to {extracted_file_name}")
                    print(f"Unzipped and renamed file: {file_name}")

                else:
                    print(f"No extracted file found for: {file_name}")

            except zipfile.BadZipFile:
                print(f"Skipping file: {file_name} (not a valid ZIP file)")
            except FileNotFoundError:
                print(f"File not found: {file_path}")

    print(f"Total files unzipped and renamed: {count}")  # Print total count of files unzipped and renamed

# Usage example
directory_path = 'ERA5Land'  # Specify the path to your directory
unzip_files_in_directory(directory_path)

