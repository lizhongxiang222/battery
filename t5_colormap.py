'''
Created on 2017年8月21日

@author: rob
'''
import numpy as np
import pylab 
import plotly
import matplotlib.pyplot as plt
import matplotlib as mpl
'''
legend_fig = plt.figure()

x = np.linspace(0, 20, 1000)
y1 = np.sin(x)
y2 = np.cos(x)

pylab.plot(x, y1, '-b', label='sine')
pylab.plot(x, y2, '-r', label='cosine')
pylab.ylim(-1.5, 2.0)

plot_url = plotly.offline.plot_mpl(legend_fig, filename='mpl-sine-cosine')
'''
mpl_color = plt.figure()

# Generate data...
nx, nsteps = 100, 20
x = np.linspace(0, 1, nx)
data = np.random.random((nx, nsteps)) - 0.5
data = data.cumsum(axis=0)
data = data.cumsum(axis=1)

# Plot
cmap = mpl.cm.gray
for i, y in enumerate(data.T):
    plt.plot(x, y, color=cmap(i / float(nsteps)))
print(i)
#print(data.T)
plot_url = plotly.offline.plot_mpl(mpl_color, filename='mpl-color-example.html')
