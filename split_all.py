import os
import glob
import shutil
import random

train_size = 550
split = 0.75

print("Creating dataset with train size (clusters number)", train_size, "and reid split (percentage)", split)

src = 'data/train/'
root_dir = 'dataset/'

# remove root_dir if present
shutil.rmtree(root_dir, ignore_errors=True)

# make directories
all_training_dir = root_dir + 'training/all/'
train_reid_training_dir = root_dir + 'training/train_reid/'
valid_reid_training_dir = root_dir + 'training/valid_reid/'
all_validation_dir = root_dir + 'validation/all/'
query_validation_dir = root_dir + 'validation/query/'
valid_validation_dir = root_dir + 'validation/valid/'

os.makedirs(all_training_dir)
os.makedirs(train_reid_training_dir)
os.makedirs(valid_reid_training_dir)
os.makedirs(all_validation_dir)
os.makedirs(query_validation_dir)
os.makedirs(valid_validation_dir)

allFileNames = os.listdir(src)
people_ids = set([name.split('_')[0] for name in allFileNames])

id_list = list(people_ids)
random.shuffle(id_list)

training_ids = id_list[:train_size]
validation_ids = id_list[train_size:]

# copy files
for p in training_ids:
    for file in glob.glob(src + p + '*'):
        shutil.copy(file, all_training_dir)

for p in training_ids:
    for file in glob.glob(src + p + '*'):
        shutil.copy(file, train_reid_training_dir)

training_dir = os.listdir(train_reid_training_dir)
vlen = int((1 - split) * len(training_dir))
random.shuffle(training_dir)
for i in range(vlen):
    shutil.move(os.path.join(train_reid_training_dir, training_dir[i]), valid_reid_training_dir)

for p in validation_ids:
    for file in glob.glob(src + p + '*'):
        shutil.copy(file, all_validation_dir)

for p in validation_ids:
    for file in glob.glob(src + p + '*'):
        shutil.copy(file, valid_validation_dir)

for p in validation_ids:
    for file in glob.glob(valid_validation_dir + p + '*'):
        shutil.move(file, query_validation_dir)
        break

print("Train data:")
print("Files in", all_training_dir, len(os.listdir(all_training_dir)))
print("Files in", train_reid_training_dir, len(os.listdir(train_reid_training_dir)))
print("Files in", valid_reid_training_dir, len(os.listdir(valid_reid_training_dir)))
print("Valid data:")
print("Files in", all_validation_dir, len(os.listdir(all_validation_dir)))
print("Files in", query_validation_dir, len(os.listdir(query_validation_dir)))
print("Files in", valid_validation_dir, len(os.listdir(valid_validation_dir)))
