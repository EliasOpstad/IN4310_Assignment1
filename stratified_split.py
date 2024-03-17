import os
import shutil
from sklearn.model_selection import train_test_split

# Create a directory for the data
data_dir = "mandatory1_data"
output_dir = "data_split"

#Define the classes (buildigns, forest, glacier, mountain, sea, street)
classes = os.listdir(data_dir)

# Create the output directories(train, val, test)
train_dir = os.path.join(output_dir, "train")
val_dir = os.path.join(output_dir, "val")
test_dir = os.path.join(output_dir, "test")

# Create the output directories (if it already exists, it will not be created again)
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

#The total number of tiles in mandatory1_data. Result from Total_images.py
total_files = 17034

# Calculate the number of images in each set
# Around 2000 images for validation and 3000 for testing and the rest for training 
validation_ratio = 2000/17034
test_ratio = 3000/17034
training_ration = 1 - validation_ratio - test_ratio

#Function to perform stratified split for each class
def stratified_split(class_dir, class_name):
    images = os.listdir(class_dir)
    # print(class_dir, class_name)
    #Calculate the number of training samples to ensure the desired split
    num_total = len(images)
    #Set the test_size within the available samples 
    test_size = int(num_total * test_ratio)
    #Set the validation_size within the available samples
    val_size = int(num_total * validation_ratio)

    #Perform the split
    train, test = train_test_split(images, test_size=test_size, random_state=42, stratify=None)
    train, val = train_test_split(train, test_size=val_size, random_state=42, stratify=None)

    for img in train:
        shutil.copy(os.path.join(class_dir, img), os.path.join(train_dir, class_name, img))
    
    for img in val:
        shutil.copy(os.path.join(class_dir, img), os.path.join(val_dir, class_name, img))

    for img in test:
        shutil.copy(os.path.join(class_dir, img), os.path.join(test_dir, class_name, img))

# Loop through the classes
for class_name in classes:
    class_dir = os.path.join(data_dir, class_name)
    # print(data_dir, class_name)
    os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
    os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)
    os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)
    stratified_split(class_dir, class_name)

print("Data split completed")

# Function to check for disjointedness
def check_disjointedness(train_dir, val_dir, test_dir):
    train_classes = os.listdir(train_dir)
    val_classes = os.listdir(val_dir)
    test_classes = os.listdir(test_dir)

    # Check for disjointedness
    for train_class in train_classes:
        train_images = set(os.listdir(os.path.join(train_dir, train_class)))
        for val_class in val_classes:
            val_images = set(os.listdir(os.path.join(val_dir, val_class)))
            assert len(train_images.intersection(val_images)) == 0, f"Images found in both train and val sets for class {train_class} and class {val_class}."

        for test_class in test_classes:
            test_images = set(os.listdir(os.path.join(test_dir, test_class)))
            assert len(train_images.intersection(test_images)) == 0, f"Images found in both train and test sets for class {train_class} and class {test_class}."
            assert len(val_images.intersection(test_images)) == 0, f"Images found in both val and test sets for class {val_class} and class {test_class}."

    print("Data split is disjointed")

check_disjointedness(train_dir, val_dir, test_dir)
