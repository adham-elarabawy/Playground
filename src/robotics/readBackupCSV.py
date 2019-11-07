import os
import csv
from datetime import datetime
import math
format = '%H:%M:%S'

with open('newscans.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    ids = []
    inHour = []
    outHour = []
    counter = 0
    for row in readCSV:
        tempID = int(row[0])
        if not (tempID in ids):
            counter += 1
        ids.append(tempID)
        inHour.append(row[2])
        outHour.append(row[3])


print(str(ids))
print(str(inHour))
print(str(outHour))

index = 0
totaled = "ID, Total Hours"
validatedIDS = []
validatedHOURS = []
for idNum in ids:
    currID = idNum
    currInHour = inHour[index]
    currOutHour = outHour[index]
    if not ((currOutHour == "") or (currInHour == "")):
        inConverted = currInHour.split(":")
        outConverted = currOutHour.split(":")
        print(outConverted)
        timeDiff = (float(outConverted[0]) - float(inConverted[0])) + \
            (float(outConverted[1]) - float(inConverted[1]))/60

        if (currID in validatedIDS):
            validatedHOURS[validatedIDS.index(currID)] += timeDiff
        else:
            validatedIDS.append(currID)
            validatedHOURS.append(timeDiff)
    index += 1

for dayNum in range(1, 7):

    with open('d' + str(dayNum) + '.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        hourAddition = 1.75
        if dayNum == 6:
            hourAddition = 1.83
        for row in readCSV:
            if (int(row[0]) in validatedIDS):
                validatedHOURS[validatedIDS.index(int(row[0]))] += hourAddition
            else:
                validatedIDS.append(int(row[0]))
                validatedHOURS.append(hourAddition)


with open('totaledHours.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    index = 0
    filewriter.writerow(['ID', 'TOTAL HOURS'])
    for m_id in validatedIDS:
        hours = "{:.1f}".format(round(validatedHOURS[index], 1))
        filewriter.writerow([m_id, hours])
        index += 1
