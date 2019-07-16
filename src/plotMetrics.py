import matplotlib.pyplot as plt

x = [0.6383, 0.6156, 0.7907, 0.6283, 0.7560, 0.7905]  # IoU
y = [0.790951, 0.846075, 0.930563, 0.928653, 0.934931, 0.949254]  # mAP
n = [1000, 2000, 3000, 4000, 'last\n(4239)', '\'highest mAP\'\n(2800)']

fig, ax = plt.subplots()
ax.scatter(x, y)

for i, txt in enumerate(n):
    ax.annotate(txt, (x[i] + 0.005, y[i] + 0.005), bbox=dict(
        boxstyle="square", fc='white', alpha=0.1))

plt.xlabel("Average Intersection over Union (IoU)")
plt.ylabel("Mean Average Precision (mAP@0.50)")
plt.title("t3 Model: IoU vs mAP")
plt.axis([0.6, 0.855, 0.775, 1])
# to emphasize difference in top ranking weights
# plt.axis([0.775, 0.8, 0.92, 0.955])
plt.show()
