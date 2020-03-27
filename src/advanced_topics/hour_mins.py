dt = 0.01  # minutes

x = 0
x1 = 0

time = 0

num_soln = 3
i = 0
hour_number = 0

thresh = 0.01  # degrees

x_prime = 6  # deg/min
x1_prime = 0.5  # deg/min

while True:
    if (x > 360):
        x -= 360
    if (x1 > 360):
        x1 -= 360
        hour_number += 1

    x += (dt * x_prime)
    x1 += (dt * x1_prime)
    time += dt

    if abs(x-x1) <= thresh:
        minutes = (x / 360) * 60
        hours = (x1 / 360) + hour_number
        print('@ {} hours & @ {} minutes'.format(round(hours), round(minutes)))
        i += 1
        if (i > num_soln):
            exit()
