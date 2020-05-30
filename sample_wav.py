import numpy as np
import matplotlib.pyplot as plt


def waveplot(f, v):
    pi = np.pi
    t = 1 / f
    plt.title('CurrentFrequency')
    plt.ylabel('VoltageRatio')
    plt.xlabel('Range:0-1 [s]')
    x = np.linspace(0, 2*pi, 1000) 
    plt.ylim(-100, 100)
    plt.xlim(0, 1000)
    y = v*(np.sin(x * f))

    plt.plot(y, color='limegreen') 
    plt.pause(0.01)  
    print("fre", round(f, 3), "[Hz]", "V", round(v, 2), "[%]", "T", round(t, 4), "[s]")

    plt.cla() 


## example of use
v = 0
f = 0 

v1 = float(input("v change rate")) 
f1 = float(input("fre change per 100ms"))
 
while 0 <= v < 100 : 
    v += v1 
    f += f1 
    waveplot(f, v) 
while 0 <= v <= 101 : 
    v -= v1 
    f -= f1 
    waveplot(f, v)