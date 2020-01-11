import os
import csv
from datetime import datetime
import math
import gspread
from oauth2client.service_account import ServiceAccountCredentials

kickoffDate = datetime.strptime('2020-1-4', '%Y-%m-%d')
format = '%H:%M:%S'

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '/Users/adhamelarabawy/Documents/Work/Robotics/Attendance_Scanner-d87a14b3476f.json', scope)
gc = gspread.authorize(credentials)

with open('input/newscans.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    ids = []
    inHour = []
    outHour = []
    scan_date = []
    counter = 0
    for row in readCSV:
        tempID = int(row[0])
        if not (tempID in ids):
            counter += 1
        ids.append(tempID)
        inHour.append(row[2])
        outHour.append(row[3])
        scan_date.append(row[1])


print(str(ids))
print(str(inHour))
print(str(outHour))

index = 0
totaled = "ID, Total Hours"
preseason_validatedIDS = []
preseason_validatedHOURS = []
buildseason_validatedIDS = []
buildseason_validatedHOURS = []
for idNum in ids:
    currID = idNum
    currInHour = inHour[index]
    currOutHour = outHour[index]
    currDate = scan_date[index]
    if not ((currOutHour == "") or (currInHour == "")):
        inConverted = currInHour.split(":")
        outConverted = currOutHour.split(":")
        print(outConverted)
        timeDiff = (float(outConverted[0]) - float(inConverted[0])) + \
            (float(outConverted[1]) - float(inConverted[1]))/60
        if (datetime.strptime(currDate, '%Y-%m-%d') < kickoffDate):
            if (currID in preseason_validatedIDS):
                preseason_validatedHOURS[preseason_validatedIDS.index(
                    currID)] += timeDiff
            else:
                preseason_validatedIDS.append(currID)
                preseason_validatedHOURS.append(timeDiff)
        else:
            if (currID in buildseason_validatedIDS):
                buildseason_validatedHOURS[buildseason_validatedIDS.index(
                    currID)] += timeDiff
            else:
                buildseason_validatedIDS.append(currID)
                buildseason_validatedHOURS.append(timeDiff)
    index += 1

for dayNum in range(1, 7):

    with open('input/d' + str(dayNum) + '.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        hourAddition = 1.75
        if dayNum == 6:
            hourAddition = 1.83
        for row in readCSV:
            if (int(row[0]) in preseason_validatedIDS):
                preseason_validatedHOURS[preseason_validatedIDS.index(
                    int(row[0]))] += hourAddition
            else:
                preseason_validatedIDS.append(int(row[0]))
                preseason_validatedHOURS.append(hourAddition)


with open('output/preseason_hours.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    index = 0
    filewriter.writerow(['ID', 'TOTAL HOURS'])
    for m_id in preseason_validatedIDS:
        hours = "{:.1f}".format(round(preseason_validatedHOURS[index], 1))
        filewriter.writerow([m_id, hours])
        index += 1

with open('output/buildseason_hours.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    index = 0
    filewriter.writerow(['ID', 'TOTAL HOURS'])
    for m_id in buildseason_validatedIDS:
        hours = "{:.1f}".format(round(buildseason_validatedHOURS[index], 1))
        filewriter.writerow([m_id, hours])
        index += 1

content = open('output/preseason_hours.csv', 'r').read()

gc.import_csv('1IW-zEbQpjJ4xDjcm_PdOr6QjNIQeZ4zISSgSNNAhlD8', content)

content = open('output/buildseason_hours.csv', 'r').read()

gc.import_csv('1sRJZoV6HGFwzzJuZhpHlncxBQ6nnVR67eHmy3Pkaclc', content)
