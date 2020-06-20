import sys
xIn = float(sys.argv[1])
xMap = [1.0, 2.0, 3.0, 4.0, 5.0]
mList = [3.0, 11.0, 52.0, 42.0]
bList = [0.0, -16.0, -139.0, -99.0]
def output(x):
	for i in range(len(xMap) - 1):
		if x >= xMap[i] and x < xMap[i + 1]:
			num = x*mList[i] + bList[i]
	try:
		return num
	except NameError:
		return "Value was outside of given range!"

print(output(xIn))