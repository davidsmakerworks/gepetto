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

import io
import wave

import openai

class Transcribe:
    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key

    def transcribe(self, audio_stream) -> str:
        '''
        Transcribe audio stream to text.

        TODO: Find a way to do this in memory without temporary file, remove magic numbers
        '''
        writer = wave.open('audio.wav', 'wb')

        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(8000)

        writer.writeframes(audio_stream)

        with open('audio.wav', 'rb') as f:
            response = openai.Audio.transcribe(model='whisper-1', file=f)

        return response['text']


class GepettoChat:
    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key

        self.reset()
        
    def reset(self) -> None:
        self._messages = [ {'role': 'system', 'content': 'You are a cheerful elderly 18th-century carpenter named GePeTto. You respond with no more than one paragraph using concise and friendly language. You are very enthutiastic about carpentry and marionettes, especially the marionette you created named Pinocchio.'} ]

    def get_chat_response(self, message: str) -> str:
        self._messages.append({'role': 'user', 'content': message})

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self._messages
        )

        self._messages.append(response['choices'][0]['message'])

        print(f'Total tokens used: {response["usage"]["total_tokens"]}')

        return response['choices'][0]['message']['content']