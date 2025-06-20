#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime
from wave import open as waveopen
from subprocess import check_output

class Speech:
    
    @staticmethod
    def get_wavfilename() ->str:
        now = datetime.now()
        name = now.strftime("%Y-%m-%d_%H-%M-%S")
        return  f"{name}.wav"
    

    @staticmethod
    def export_wav(filepath, pcm, channels=1, rate=24000, sample_width=2):
        with waveopen(filepath, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)

