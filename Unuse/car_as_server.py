import matplotlib.pyplot as plt
import numpy as np
import math

fig = plt.figure()
theta = np.arange(0, 2 * math.pi, 0.01)
center1 = [50, 50]
x1 = 5 * np.cos(theta) + center1[0]
y1 = 5 * np.sin(theta) + center1[1]
center2 = [60, 60]
x2 = 10 * np.cos(theta) + center2[0]
y2 = 10 * np.sin(theta) + center2[1]
plt.plot(x1, y1, '-r', x2, y2, '--b')
plt.show()



