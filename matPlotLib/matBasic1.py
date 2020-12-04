import matplotlib.pyplot as plt
import numpy as np
#x = np.arange(-4, 4, .1)
x = np.linspace(0, 2*np.pi, 50)
y = np.sin(x)
y2 = np.cos(x - np.pi/2)
#y3 = x * x -2
plt.plot(x, y,  'bo', linewidth=3, markersize=7, label='sin')
plt.plot(x, y2, 'r-', linewidth=3, markersize=7, label='cos')
#plt.plot(x, y3, 'g-o', linewidth=3, markersize=7, label='green')
plt.legend(loc='upper center')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Graph')
#plt.axis([0, 5, 2, 11])
plt.grid(True)
plt.show()
