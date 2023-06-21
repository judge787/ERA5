import os

# Set the city variable to "London"
city = "Guelph"
province = "ON"
lat = "43.60"
lon = "-80.50"
first = "0.5,,,,"
second = "1.0,,,,"
third = "1.5,,,,"
timeOffset = "-5.0"

location = f"{city}, {province}"
print(location)

def replaceDays(start, end):
    output_file_path = f"{location}/Modified EPW Files/ERA5_{city}_Dec{year}.epw"
    with open(output_file_path, 'r') as output_file:
        # Read the lines of the file into a list
        lines = output_file.readlines()

    # Get the line to copy from
    line_to_copy = lines[start - 1]

    # Loop through the specified lines
    for i in range(start, end):
        # Get the line to modify
        line_to_modify = lines[i]

        # Replace the 8th and 9th characters with the corresponding characters from line 745
        line_to_modify = line_to_modify[:7] + line_to_copy[7:9] + line_to_modify[9:]

        # Write the modified line back to the list
        lines[i] = line_to_modify
    
    with open(output_file_path, 'w') as output_file:
        # Write the modified lines back to the file
        output_file.writelines(lines)

def replaceDaysTwoDigits(start, end):
    output_file_path = f"{location}/Modified EPW Files/ERA5_{city}_Dec{year}.epw"
    # with open(output_file_path, 'r') as output_file:
    #     # Read the lines of the file into a list
    #     lines = output_file.readlines()

    # with open(output_file_path, 'w') as output_file:
    #     # Write the unmodified lines back to the file
    #     output_file.writelines(lines)

    with open(output_file_path, 'r') as output_file:
        lines = output_file.readlines()

    # Get the line to copy from
    line_to_copy = lines[start - 1]

    # Loop through the specified lines
    for i in range(start, end):
        # Get the line to modify
        line_to_modify = lines[i]

        # Replace the 8th and 9th characters with the corresponding characters from line 745
        line_to_modify = line_to_modify[:8] + line_to_copy[8:10] + line_to_modify[10:]

        # Write the modified line back to the list
        lines[i] = line_to_modify
    
    with open(output_file_path, 'w') as output_file:
        # Write the modified lines back to the file
        output_file.writelines(lines)


for year in range(2007, 2021):
    # Define the paths to the input and output files for the current year
    input_file_path = f"{location}/EPW Files/{year}/ERA5_{city}_Dec{year}.epw"
    output_file_path = f"{location}/Modified EPW Files/ERA5_{city}_Dec{year}.epw"
    output_original_path = f"{location}/EPW Files/{year}/ERA5_{city}_Dec{year}.epw"

    # Check if the output directory exists, and create it if it doesn't
    if not os.path.exists(f"{location}/Modified EPW Files"):
        os.makedirs(f"{location}/Modified EPW Files")

    # Open the input EPW file for reading
    with open(input_file_path, 'r') as input_file:
        # Read the lines of the file into a list
        lines = input_file.readlines()

    # Get the first line of the file
    first_line = lines[0]

    # Split the line into a list of values
    values = first_line.split(',')

    # Replace the 2nd value with the value of the city variable
    values[1] = city
    # Replace the 3rd value with the value of the province variable
    values[2] = province
    # Replace the 7th value with the value of the lat variable
    values[6] = lat
    # Replace the 8th value with the value of the lon variable
    values[7] = lon
    # Replace the 9th value with the value of the timeOffset variable
    values[8] = timeOffset
   

    # Join the list of values back into a string
    first_line = ','.join(values)

    # Write the modified first line back to the list
    lines[0] = first_line
    # Iterate over the range of years from 1981 to 1999

   
    if 'H' in lines[3]:
        # Find the index of the character 'H' in line 4
        index = lines[3].index('H')
        # Insert a newline after the character 'H'
        lines[3] = lines[3][:index] + '\n' + lines[3][index:]
    # else:
    #     print("H not found.")

    if "0.035,,,," in lines[3]:
        # Replace "0.035,,,," with the value of the first variable
        lines[3] = lines[3].replace("0.035,,,,", first)
    # else:
    #     print("Variable 1 not found.")
    
    if "0.175,,,," in lines[3]:
        # Replace "0.175,,,," with the value of the second variable
        lines[3] = lines[3].replace("0.175,,,,", second)
    # else:
        # print("Variable 2 not found.")

    if "0.64,,,," in lines[3]:
        # Replace "0.64,,,," with the value of the third variable
        lines[3] = lines[3].replace("0.64,,,,", third)
    # else:
        # print("Variable 3 not found.")



    with open(output_file_path, 'w') as output_file:
        # Write the modified lines back to the file
        output_file.writelines(lines)

    # with open(output_file_path, 'r') as output_file:
    #     # Read the lines of the file into a list
    #     lines = output_file.readlines()

    with open(output_file_path, 'r') as input_file:
    #Read the lines of the file into a list
        lines = input_file.readlines()

    # Replace lines 747-752 with the contents of lines 723-728
    lines[746:752] = lines[722:728]
    lines[1418:1424] = lines[1394:1400]
    lines[2162:2168] = lines[2138:2144]
    lines[2882:2888] = lines[2858:2864]
    lines[3626:3632] = lines[3602:3608]
    lines[4346:4352] = lines[4322:4328]
    lines[5090:5096] = lines[5066:5072]
    lines[5834:5840] = lines[5810:5816]
    lines[6554:6560] = lines[6530:6536]
    lines[7298:7304] = lines[7274:7280]
    lines[8018:8024] = lines[7994:8000]
    lines[8761:8788]= lines[8737:8744]
    # Open the output EPW file for writing
    with open(output_file_path, 'w') as output_file:
        # Write the modified lines back to the file
        output_file.writelines(lines)

    # call the replaceDays function for months that are single digits 
    replaceDays(746, 752) #January
    replaceDays(1418, 1424) #Feburary
    replaceDays(2162, 2168) #March
    replaceDays(2882, 2888) #April
    replaceDays(3626, 3632) #May
    replaceDays(4346, 4352) #June
    replaceDays(5090, 5096) #July
    replaceDays(5834, 5840) #August
    replaceDays(6554, 6560) #September

    #call the replaceDays function for months that are double digits
    replaceDaysTwoDigits(7298, 7304) #October
    replaceDaysTwoDigits(8018, 8024) #November
    replaceDaysTwoDigits(8761, 8768) #December