import sys
import re
import numpy as np

outFName = sys.argv[3]

xMap = []
yMap = []
mList = []
bList = []

inX = open(sys.argv[1], "r")

line = inX.readline()
xList = re.split(",", line)
inX.close()

inY = open(sys.argv[2], "r")

line = inY.readline()
yList = re.split(",", line)
inY.close()

if len(xList) != len(yList):
	print("You're bad the two inputs don't have the same length")
	1 / 0

for ele in xList:
	xMap.append(float(ele))

for ele in yList:
	yMap.append(float(ele))

print(xMap)
print(yMap)

x_ = xMap[0]
y_ = yMap [0]

for i in range(len(xMap) - 1):
	x_i = xMap[i+1]
	y_i = yMap[i+1]
	m_ = (y_i - y_) / (x_i - x_)
	mList.append(m_)
	b_ = y_i - m_*x_i
	bList.append(b_)
	x_ = x_i
	y_ = y_i

for i in range(len(xMap) - 1):
	print("y = " + str(mList[i]) + "x + " + str(bList[i]))

text = """\
import sys\n\
xIn = float(sys.argv[1])\n\
xMap = """ + str(xMap) + """\n\
mList = """ + str(mList) + """\n\
bList = """ + str(bList) + """\n\
def output(x):\n\
\tfor i in range(len(xMap) - 1):\n\
\t\tif x >= xMap[i] and x < xMap[i + 1]:\n\
\t\t\tnum = x*mList[i] + bList[i]\n\
\ttry:\n\
\t\treturn num\n\
\texcept NameError:\n\
\t\treturn "Value was outside of given range!"\n\n\
print(output(xIn))\
"""

print(text)

outFile = open(outFName, "w+")
outFile.write(text)
outFile.close()

with open("pw_lin_interp_mList.csv", "w+") as outFile:
	for i in range(len(mList)):
		if i != 0:
			outFile.write(",")
		outFile.write(str(mList[i]))

with open("pw_lin_interp_bList.csv", "w+") as outFile:
    for i in range(len(bList)):
        if i != 0:
            outFile.write(",")
        outFile.write(str(bList[i]))

lin = np.polyfit(xMap, yMap, 1)

np.polyfit(xMap, yMap, 2, full=False)

