from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import json

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

errorResult = json.load(open('error.json', 'r'))
i = 0
xs = []
ys = []
zs = []
for x in range(1, 1000, 10):
    for y in range(1, 1000, 10):
        xs.append(x)
        ys.append(y)
        zs.append(errorResult[i])
        i += 1
# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].


for c, m, zlow, zhigh in [('b', '^', 123623, 843845)]:
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.savefig('error.png')
plt.show()