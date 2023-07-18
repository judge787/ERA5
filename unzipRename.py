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

#                 # Rename the extracted file to match the ZIP file name
#                 extracted_file_name = os.path.splitext(file_name)[0] + ".nc"
#                 extracted_file_path = os.path.join(directory, extracted_file_name)
                
#                 print(f"\n{count + 1}. Extracted file name: {extracted_file_name} and path: {extracted_file_path}")

#                 # Find the extracted file and rename it
#                 extracted_files = [f for f in os.listdir(directory) if f.endswith('.nc')]
#                 print(f"Second extraction: {extracted_files}")
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
# directory_path = '1980'  # Specify the path to your directory
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
                    # Extract the contents into a new subdirectory with the same name as the ZIP file
                    zip_ref.extractall(os.path.join(directory, os.path.splitext(file_name)[0]))

                # Rename the extracted file to match the ZIP file name
                extracted_file_name = os.path.splitext(file_name)[0] + ".nc"
                extracted_file_path = os.path.join(directory, extracted_file_name)
                
                print(f"\n{count + 1}. Extracted file name: {extracted_file_name} and path: {extracted_file_path}")

                # Find the extracted file and rename it
                extracted_files = [f for f in os.listdir(os.path.join(directory, os.path.splitext(file_name)[0])) if f.endswith('.nc')]
                print(f"Second extraction: {extracted_files}")
                if len(extracted_files) > 0:
                    count += 1
                    for extracted_file in extracted_files:
                        extracted_file_old_path = os.path.join(directory, os.path.splitext(file_name)[0], extracted_file)
                        os.rename(extracted_file_old_path, extracted_file_path)
                        print(f"Renamed file: {extracted_file} to {extracted_file_name}")
                        print(f"Unzipped and renamed file: {file_name}")
                else:
                    print(f"No extracted file found for: {file_name}")

                # Delete the subdirectory
                subdirectory_path = os.path.join(directory, os.path.splitext(file_name)[0])
                os.rmdir(subdirectory_path)
                print(f"Deleted subdirectory: {subdirectory_path}")

            except zipfile.BadZipFile:
                print(f"Skipping file: {file_name} (not a valid ZIP file)")
            except FileNotFoundError:
                print(f"File not found: {file_path}")

    print(f"Total files unzipped and renamed: {count}")  # Print total count of files unzipped and renamed

# Usage example
city = "St. John's"
province = "NL"
location = f"{city}, {province}"

directory_path = f"{location}/ERA5Land"  # Specify the path to your directory
unzip_files_in_directory(directory_path)