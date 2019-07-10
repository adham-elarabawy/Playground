# author: Adham Elarabawy
# date: 7/9/2019
# use-case: to split many annotated files into a test and train dataset

#--NOTES--#
# make sure that you're using absolute paths, not relative paths. It doesn't/shouldn't matter where this script is placed.
# make sure that there are no subdirectories in the 'imageDir' path
# make sure that you create the train and test folders BEFORE running the script


#--IMPORTS--#
import random
import shutil
import os

#--CONFIG--#
VERSION_NUMBER = 2
dataServerLocation = "/mnt/nas01/workspace_share/cnn/yolo/darknet/data/t" + \
    str(VERSION_NUMBER)  # + "/test/"
defaultMarkTrainPath = "x64/Release/data/img/"
# in yolo_mark, this is your data/img:
imageDir = "/Users/adhamelarabawy/Documents/GitHub/Yolo_mark/x64/Release/data/t2/img"
trainDir = "/Users/adhamelarabawy/Documents/GitHub/Yolo_mark/x64/Release/data/t2/train"
testDir = "/Users/adhamelarabawy/Documents/GitHub/Yolo_mark/x64/Release/data/t2/test"
# this means that the test dataset(testDir) will be 20% the original size of the original dataset(imageDir)
testPercent = 0.2
imgType = "jpg"
textType = "txt"

#--SPLITTING--#
files = os.listdir(imageDir)
numOfFiles = (len(files) - 1) / 1
numOfImages = numOfFiles / 2

print("# of files:", numOfFiles)
print("# of images:", numOfImages)

# move all files to train
for f in files:
    shutil.copy(imageDir+"/"+str(f), trainDir+"/"+str(f))

testNumOfImages = int(round(testPercent*numOfImages))

print("# of images in test:", testNumOfImages)

shuffledFiles = random.sample(files, len(files))
testList = []
tempIndex = 0

testFile = open(testDir+"."+textType, "w")
for file in shuffledFiles:
    if file[-len(imgType):] == imgType:
        testList.append(file)
        testFile.write(dataServerLocation + "/test/" + file + "\n")
        tempIndex += 1
    if(tempIndex == testNumOfImages):
        testFile.close()
        break


for file in testList:
    # file at current index is always a string in this loop
    foundFile = str(file)
    remainingFile = str(
        file[:-len(imgType)] + textType)
    for tempFile in files:
        if str(tempFile) == remainingFile:
            shutil.move(trainDir+"/"+foundFile, testDir+"/"+foundFile)
            shutil.move(trainDir+"/"+remainingFile,
                        testDir+"/"+remainingFile)
            break
    else:
        print("FATAL ERROR(0): UNABLE TO FIND MATCHING TEXT FILE FOR IMAGE @:")
        print("Found File: ", foundFile)
        print("Remaining File: ", remainingFile)
        break

# remove images in test dataset from train text file
for file in testList:
    strippedFile = file[:-len(imgType)]
    print(strippedFile)
    fn = trainDir+"."+textType
    output = open(fn).readlines()
    t = open(fn, 'w')
    t.writelines([item for item in output if str(strippedFile) not in item])
    t.close()

# fix the train text file paths:
# Read in the file
with open(fn, 'r') as file:
    filedata = file.read()

# Replace the target string
filedata = filedata.replace(
    defaultMarkTrainPath, dataServerLocation + "/train/")

# Write the file out again
with open(fn, 'w') as file:
    file.write(filedata)
