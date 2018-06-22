import alsaaudio
import audioop
import time
from struct import unpack
import numpy as np

DEFAULT_NUM_CHANNELS=1
DEFAULT_SAMPLE_RATE=8000
DEFAULT_FPS=160

class Microphone:

    num_channels=DEFAULT_NUM_CHANNELS
    sample_rate=DEFAULT_SAMPLE_RATE
    frame_rate=DEFAULT_FPS

    # Set up audio
    '''
    sample_rate = 9600
    no_channels = 1
    chunk = 4096 # Use a multiple of 8
    data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)
    data_in.setchannels(no_channels)
    data_in.setrate(sample_rate)
    data_in.setformat(aa.PCM_FORMAT_S16_LE)
    data_in.setperiodsize(chunk)
    '''

    def __init__(self,nc=None,sr=None,fps=None):

        # Redefine parameters from input:
        if nc is not None:self.num_channels=nc
        if sr is not None:self.sample_rate=sr
        if fps is not None:self.frame_rate=fps

        # Create microphone poller
        self.mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

        self.mic.setchannels(self.num_channels)
        self.mic.setrate(self.sample_rate)

        ## 16-bit little endian format
        self.mic.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.mic.setperiodsize(self.frame_rate)

    def set_frame_rate(self,new_fps):
        self.frame_rate=new_fps

    def get_frame_rate(self):
        return self.frame_rate

    def set_sample_rate(self,new_sr):
        self.sample_rate=new_sr

    def get_sample_rate(self):
        return self.sample_rate


    # External parent process will pass Queue
    def listen(self,queue):
        while True:
            print"Listening"
            self.mic.setperiodsize(self.frame_rate)
            print"Frame Rate Set"
            l,d = self.mic.read()
            print "Mic Read"
            queue.put_nowait(d)
            print"Pushed"
            #time.sleep(float(1.0/sample_rate))
            time.sleep(0.001)
        print "Break"
