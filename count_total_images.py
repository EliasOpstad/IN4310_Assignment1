import os

#Function to count the number of images in a directory
def count_images(directory):
    jpg_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".jpg"):
                jpg_count += 1
    return jpg_count


#Path to the directories
mandatory1_data_path = "mandatory1_data"
data_split_path = "data_split"

#Count the number of images in the directories
mandatory1_data_count = count_images(mandatory1_data_path)
data_split_count = count_images(data_split_path)

#Print the results
print("Total images in mandatory1_data:", mandatory1_data_count)
print("Total images in data_split:", data_split_count)

#Count the number of images in each subdirectory
subdirectory_paths = [os.path.join(data_split_path, subdir) for subdir in os.listdir(data_split_path)]
for subdirectory_path in subdirectory_paths:
    subdirectory_count = count_images(subdirectory_path)
    print("Total images in", subdirectory_path, ":", subdirectory_count)
