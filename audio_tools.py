# MIT License

# Copyright (c) 2023 David Rice

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import array

import pyaudio

from typing import Tuple


class AudioPlayer:
    def __init__(self) -> None:
        self._pyaudio = pyaudio.PyAudio()
        self._stream = self._pyaudio.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)

    def play(self, audio_stream) -> None:
        self._stream.write(audio_stream)

    def close(self) -> None:
        self._stream.stop_stream()
        self._stream.close()
        self._pyaudio.terminate()


class AudioRecorder:
    def __init__(self) -> None:
        self._pyaudio = pyaudio.PyAudio()
        self._stream = self._pyaudio.open(format=pyaudio.paInt16, channels=1, rate=8000, input=True)

    def record(self, max_duration: int) -> Tuple[bytes, bool]:
        '''
        Record audio for up to max_duration seconds.
        
        Returns:
            bytes: Audio stream
            bool: True if valid audio was recorded, False otherwise
            
        TODO: Remove magic numbers

        TODO: Improve silence detection

        TODO: Trim pre-audio silence
        '''
        frames = []
        num_frames = 0
        silent_frames = 0
        silence_detected = False
        was_silent = True

        max_frames = int(max_duration * 8000 / 1024)
        
        while (num_frames < max_frames) and not silence_detected:
            num_frames += 1
            data = self._stream.read(1024)
            data_array = array.array('h', data)

            if max(data_array) < 500:
                if was_silent:
                    silent_frames += 1
                was_silent = True
            else:
                silent_frames = 0
                was_silent = False

            frames.append(data)

            if silent_frames > 10:
                silence_detected = True

        if num_frames < 18:
            valid_audio = False
        else:
            valid_audio = True

        return (b''.join(frames[:-10]), valid_audio)

    def close(self) -> None:
        self._stream.stop_stream()
        self._stream.close()
        self._pyaudio.terminate()