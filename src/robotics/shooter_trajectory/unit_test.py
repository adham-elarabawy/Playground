import math

# all distances are in inches
h = 98.25 #height of center of inner port
offset = 29.25 #inner port is deeper in the tower
g = -386.221 #gravitational acceleration, in/s^2

def theta(d):
	return math.atan(2*h/d)

def v_0(theta):
	return math.sqrt(-2*g*h) / math.sin(theta)

print("distance  theta  velocity")
with open("apogee_hit.csv", "w+") as file:
	file.write("distance,theta,velocity\n")
	for d in range(1, 361):
		th = theta(d + offset)
		print(str(d) + "  " + str(math.degrees(th)) + "  " + str(v_0(th)) + "\n")
		file.write(str(d) + "," + str(math.degrees(th)) + "," + str(v_0(th)) + "\n")
