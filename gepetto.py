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

import os

from audio_tools import AudioPlayer, AudioRecorder
from azure_tools import AzureSpeech
from openai_tools import Transcribe, GepettoChat


def main() -> None:
    try:
        azure_speech_region = os.environ['AZURE_SPEECH_REGION']
        azure_speech_key = os.environ['AZURE_SPEECH_KEY']

        openai_api_key = os.environ['OPENAI_API_KEY']
    except KeyError:
        print('Missing environment variables. Please set the following:')
        print('AZURE_SPEECH_REGION')
        print('AZURE_SPEECH_KEY')
        print('OPENAI_API_KEY')
        return

    audio_player = AudioPlayer()
    transcriber = Transcribe(api_key=openai_api_key)
    azure_speech = AzureSpeech(
        subscription_key=azure_speech_key,
        region=azure_speech_region)

    gepetto_chat = GepettoChat(openai_api_key)

    print('Welcome to GePeTto! Use your voice to chat with this AI carpenter character.\n')

    while True:
        input('---Press ENTER to start new conversation---')
        gepetto_chat.reset()
        silent_loops = 0

        while silent_loops < 10:         
            print('Recording for up to 15 seconds...')
            audio_recorder = AudioRecorder()

            (in_stream, valid_audio) = audio_recorder.record(15)
            audio_recorder.close()

            if valid_audio:
                print('Transcribing...')
                msg = transcriber.transcribe(in_stream)

                print('Getting chat response...')
                response = gepetto_chat.get_chat_response(msg)

                print('Playing response...')
                tts_stream = azure_speech.text_to_speech(response)
                audio_player.play(tts_stream)

                silent_loops = 0
            else:
                print('No audio detected. Try again.')
                silent_loops += 1


if __name__ == '__main__':
    main()