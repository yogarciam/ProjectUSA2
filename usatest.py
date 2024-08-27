import numpy as np
import sounddevice as sd
from PyDAQmx import Task
import PyDAQmx as daq

class DAQSystem:
    def __init__(self):
        self.task = Task()
        self.sample_rate = 44100
        self.duration = 10  # seconds
        self.channels = 4
        self.data = np.zeros((self.sample_rate * self.duration, self.channels))

    def configure_daq(self):
        for i in range(self.channels):
            self.task.CreateAIVoltageChan(f"Dev1/ai{i}", "", daq.DAQmx_Val_RSE, -10.0, 10.0, daq.DAQmx_Val_Volts, None)
        self.task.CfgSampClkTiming("", self.sample_rate, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, self.sample_rate * self.duration)

    def start_acquisition(self):
        self.configure_daq()
        self.task.StartTask()
        read = daq.int32()
        self.task.ReadAnalogF64(self.sample_rate * self.duration, 10.0, daq.DAQmx_Val_GroupByChannel, self.data, self.data.size, daq.byref(read), None)
        print("Acquisition complete")

    def stop_acquisition(self):
        self.task.StopTask()
        self.task.ClearTask()

    def play_sound(self):
        fs = 44100  # Sampling rate
        duration = 5  # seconds
        t = np.linspace(0, duration, int(fs*duration), endpoint=False)
        sound = np.sin(2 * np.pi * 440 * t)  # Generate a 440 Hz tone
        sd.play(sound, fs)
        sd.wait()

if __name__ == "__main__":
    daq_system = DAQSystem()
    
    # Start Data Acquisition
    daq_system.start_acquisition()
    
    # Play Sound
    daq_system.play_sound()
    
    # Stop Data Acquisition
    daq_system.stop_acquisition()
print(daq_system)