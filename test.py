#!/usr/bin/env python

import alsaaudio as aa
from time import sleep
from struct import unpack
import numpy as np
from matplotlib import pyplot as plt

# Set up audio
sample_rate = 16000
no_channels = 1
chunk =  320# Use a multiple of 8
data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)
data_in.setchannels(no_channels)
data_in.setrate(sample_rate)
data_in.setformat(aa.PCM_FORMAT_S16_LE)
data_in.setperiodsize(chunk)

def calculate_levels(data):
   # Convert raw data to numpy array
    data = unpack("%dh"%((len(data)/2)),data)
    data = np.array(data, dtype='h')
   # Apply FFT - real data so rfft used
    fourier=np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
    fourier=np.delete(fourier,len(fourier)-1)
   # Find amplitude
    power = (np.log10(np.abs(fourier))**2)-5
    '''
    for i in range (0,len(fourier)):
    #for i in range (4,50):
        for stars in range(0,int(power[i])):
                print "*",
        print ""
    print "End"
    '''
    return power


plt.ion()

fig = plt.figure()
plot = fig.add_subplot(111)

xdata = np.linspace(0,sample_rate,chunk/2)
ydata = np.zeros(chunk/2,dtype=float)
line, = plot.plot(xdata,ydata,'-')
plot.set_ylim(-20,100)



while True:
   # Read data
   data_in.setperiodsize(chunk)
   l,data = data_in.read()
   power = calculate_levels(data)
   line.set_ydata(power)
   fig.canvas.draw()
