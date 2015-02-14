#!/usr/bin/env python
import sys
from pylab import *
import wave

def show_wave_n_spec(speech):
    spf = wave.open(speech,'r')
    sound_info = spf.readframes(-1)
    sound_info = fromstring(sound_info, 'Int16')

    f = spf.getframerate()

    subplot(211)
    plot(sound_info)
    title('Wave from and spectrogram of %s' % speech)

    subplot(212)
    spectrogram = specgram(sound_info, Fs = f, scale_by_freq=True,sides='default')

    show()
    spf.close()
def bin(waveform, binFactor):
    max=0
    newWaveform=list()
    for i in range(0,len(waveform)//binFactor):
        for j in range(0,binFactor):
            if(abs(waveform[i*binFactor+j])>max):
                max=abs(waveform[i*binFactor+j])
        newWaveform+=[max]
        max=0
    return newWaveform
def findPeaks(waveform,cutOff, minDist):
    peaks=list()
    for i in range(1,len(waveform)-1):
        if (waveform[i-1]<waveform[i] and waveform[i+1]<waveform[i] and waveform[i]>cutOff):#First check if it is a relative maximum
            if len(peaks)==0:
                peaks+=[i]
            elif i-peaks[-1]>minDist:
                peaks+=[i]
            elif waveform[i]>waveform[peaks[-1]]:
                peaks[-1]=i
    return peaks






file = "audio_work/backgroundnoise.wav"

spf = wave.open(file,'r')
sound_info = spf.readframes(-1)
sound_info = fromstring(sound_info, 'Int16')
subplot(211)
plot(sound_info)
print("adsa")
newWaveform=bin(sound_info,1000)
subplot(212)
plot(newWaveform)
show()