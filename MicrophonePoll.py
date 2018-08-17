import alsaaudio
import time
from struct import unpack
import numpy as np

DEFAULT_NUM_CHANNELS = 1
DEFAULT_SAMPLE_RATE = 32000
DEFAULT_FPS = 1280


class Microphone:

    num_channels = DEFAULT_NUM_CHANNELS
    sample_rate = DEFAULT_SAMPLE_RATE
    frame_rate = DEFAULT_FPS

    @staticmethod
    def test():
        mic = Microphone()
        while True:
            print mic.get_data()


    def __init__(self, nc=None, sr=None, fps=None):

        # Redefine parameters from input:
        if nc is not None:
            self.num_channels = nc
        if sr is not None:
            self.sample_rate = sr
        if fps is not None:
            self.frame_rate = fps
        self.mic = None
        self.setup()

    def setup(self):
        self.mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        self.mic.setchannels(self.num_channels)
        self.mic.setrate(self.sample_rate)

        # 16-bit little endian format
        self.mic.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.mic.setperiodsize(self.frame_rate)

        self.changed = False

    def set_frame_rate(self, new_fps):
        self.frame_rate = new_fps
        # self.changed = True

    def get_frame_rate(self):
        return self.frame_rate

    def set_sample_rate(self, new_sr):
        self.sample_rate = new_sr
        self.changed = True

    def get_sample_rate(self):
        return self.sample_rate

    def get_data(self):
        self.mic.setperiodsize(self.frame_rate)
        return self.mic.read()

if __name__ == "__main__":
    Microphone.test()
