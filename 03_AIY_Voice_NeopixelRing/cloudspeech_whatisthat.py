#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""

import argparse
import locale
import logging
import subprocess
import aiy
import whatisthat
import picamera

from PIL import Image

from aiy.voice import tts
from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient

def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('what is that',
                'what logo is that',
                'what does that say',
                'goodbye')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Vision & Speech Demo')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
        while True:
            board.led.state = Led.PULSE_QUICK
            if hints:
                logging.info('Push the button & show me something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Push the button & show me something.')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            
            board.button.wait_for_press()
            
            if text is None:
                logging.info('Sorry, what was that?')
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower()
            if 'what is that' in text:
                output = whatisthat.takeAndProcessImage('label')
            elif 'what logo is that' in text:
                output = whatisthat.takeAndProcessImage('logo')
            elif 'what does that say' in text:
                output = whatisthat.takeAndProcessImage('text')
            elif 'goodbye' in text:
                break
            
            # If we got a result then both print and speak it. 
            if output is not None:
                print(output)
                aiy.voice.tts(output)

if __name__ == '__main__':
    main()