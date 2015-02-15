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
def findPeaks(waveform,cutOff, minDist):#returns the peaks in aplitude of sound, where 0 is begining of recording and 1 is the end
    peaks=list()
    for i in range(1,len(waveform)-1):
        if (waveform[i-1]<waveform[i] and waveform[i+1]<waveform[i] and waveform[i]>cutOff):#First check if it is a relative maximum
            if len(peaks)==0:
                peaks+=[i]
            elif i-peaks[-1]>minDist:
                peaks+=[i]
            elif waveform[i]>waveform[peaks[-1]]:
                peaks[-1]=i
    return [j/len(waveform) for j in peaks]
def lengthOfWave(wave):
    frames = wave.getnframes()
    rate = wave.getframerate()
    duration = frames / float(rate)
    return duration

def intensityAtFrequencies(spf,freqLow,freqHigh):
    result=list()
    sound_info = spf.readframes(-1)
    sound_info = fromstring(sound_info, 'Int16')
    f = spf.getframerate()
    spectrogram= specgram(sound_info, Fs = f, scale_by_freq=True,sides='default')
    sum=0
    for t in range(0,len(spectrogram[2])):
        for freq in range(freqLow,freqHigh):
            sum+=spectrogram[0][freq,t]
        result+=[sum]
        sum=0
    return result

def findHit(spect,freq):#return the time the cue ball strikes the rack as a fraction of where it is in the recording
    frequency=spect[0][122,:]
    max=0
    for i in range(0,len(frequency)):
        if frequency[i]>frequency[max]:
            max=i
    return max/len(frequency)
def indexOfClosestValue(list,value):
    min=0
    for i in range(0,len(list)):
        if abs(list[i]-value)<abs(list[min]-value):
            min=i
    if abs(list[min]-value)>0.02:
        print("WARNING: peaks not lining up, results may be inaccurate")
    return min
def findBreakSpeed(file):
    spf = wave.open(file,'r')
    sound_info = spf.readframes(-1)
    sound_info = fromstring(sound_info, 'Int16')
    f = spf.getframerate()

    spectrogram= specgram(sound_info, Fs = f, scale_by_freq=True,sides='default')

    newWaveform=bin(sound_info,1000)

    peaks=findPeaks(newWaveform,max(newWaveform)//2,10)
    hit2=findHit(spectrogram,122)
    print(peaks)
    print(hit2)
    subplot(211)
    plot(newWaveform)
    subplot(212)
    plot(spectrogram[0][122,:])
    show()
    print(indexOfClosestValue(peaks,hit2))

findBreakSpeed("audio_work/backgroundnoise_30cm.wav")
