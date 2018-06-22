#!/usr/bin/env python

from Tkinter import *
import alsaaudio as aa
from time import sleep
from struct import unpack
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
matplotlib.use('TkAgg')


# Set up audio
sample_rate = 16000
no_channels = 1
chunk =  640# Use a multiple of 8
waterfallframes=2000
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
    return power



root = Tk()

mainframe = PanedWindow(root,orient=VERTICAL,showhandle=True,bg='black')


wftFrame=Frame(mainframe)

fig = plt.figure()
plot = fig.add_subplot(111)

xdata = np.linspace(0,chunk/2,chunk/2)
ydata = np.zeros(chunk/2,dtype=float)
waterfalldata=np.zeros([chunk/2,waterfallframes],dtype=float)

line, = plot.plot(xdata,ydata,'-',color='green')
plot.set_ylim(0,2000)

canvas = FigureCanvasTkAgg(fig,master=wftFrame)
plotwidg=canvas.get_tk_widget()

toolbar = NavigationToolbar2TkAgg(canvas, wftFrame)
toolbar.update()
#canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

wfplot=fig.add_subplot(111)
waterfalldata=np.zeros([waterfallframes,chunk/2],dtype=float)
im = wfplot.imshow(waterfalldata,interpolation='nearest',origin='bottom',aspect='auto',vmin=-10,vmax=20,cmap='bone')
wfcanvas=FigureCanvasTkAgg(fig,master=wftFrame)
wfwidg=wfcanvas.get_tk_widget()
wfwidg.pack(side=TOP,fill=BOTH,expand=True)


mainframe.add(wftFrame)

mainframe.pack(side=TOP)
root.title("Audio Plots")

timer=waterfallframes
fig.canvas.draw()
while True:
   timer-=1
   # Read data
   data_in.setperiodsize(chunk)
   l,data = data_in.read()
   power = calculate_levels(data)
   waterfalldata[timer]=power
   line.set_data(xdata,(power*20)+100)
   im.set_data(waterfalldata)
   fig.canvas.draw()
   if timer==0:timer=waterfallframes


root.mainloop()
