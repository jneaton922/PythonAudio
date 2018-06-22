import MicrophonePoll
from multiprocessing import Process,Queue
import numpy as np
from Tkinter import *
from struct import unpack
import time





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
    for i in range (0,len(fourier)):
    #for i in range (4,50):
        for stars in range(0,int(power[i])):
                print "*",
        print ""
    print "End"
    return


def main():
    mic = MicrophonePoll.Microphone()
    dataQueue=Queue()
    mic_process = Process(target=mic.listen,args=(dataQueue,))
    mic_process.start()

    while True:
        if not dataQueue.empty():
            calculate_levels(dataQueue.get_nowait())
        else:
            time.sleep(.001)


if __name__ == "__main__":
    main()
