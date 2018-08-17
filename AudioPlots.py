import MicrophonePoll
import numpy as np
from Tkinter import *
from struct import unpack


def calculate_levels(data):
    #  Convert raw data to numpy array
    data = unpack("%dh" % ((len(data)/2)), data)
    data = np.array(data, dtype='h')
    # Apply FFT - real data so rfft used
    fourier = np.fft.rfft(data)
    #  Remove last element in array to make it the same size as chunk
    fourier = np.delete(fourier, len(fourier)-1)
    #  Find amplitude
    power = (np.log10(np.abs(fourier))**2)-5

    for i in range(0, len(fourier)):
        for stars in range(0, int(power[i])):
                print "*",
        print ""
    print "End"
    return


def main():
    mic = MicrophonePoll.Microphone(sr=8000, fps=160)
    mic.setup()

    while True:
        # print "LOOP"
        calculate_levels(mic.get_data()[1])


if __name__ == "__main__":
    main()
