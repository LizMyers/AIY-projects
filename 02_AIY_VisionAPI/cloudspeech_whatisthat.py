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
import random
import time

from time import sleep
from PIL import Image
from random import choice
from aiy.voice import tts
from aiy.voice.audio import AudioFormat, play_wav
from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient

#subsitute your first name below
firstName = 'friend'

def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('what is that',
                'what\'s that',
                'what is there',
                'what logo is that',
                'what logo is there',
                'whose logo is that',
                'what does that say',
                'can you read that',
                'help',
                'thank you',
                'thanks',
                'well done',
                'great, thanks',
                'goodbye',
                'so long',
                'stop')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language
    
def random_error():
    errorArray = ['Sorry, I didn\'t catch that, please try again', 
                'Sorry, what was that?',
                'Oh dear. I didn\'t quite get that. Please try again.', 
                'Bummer, I messed up. Please try again.',
                'Whoops a daisy, I didn\'t quite get that, please try again.']
    rand_error = random.choice(errorArray)
    return rand_error

def random_help():
    helpArray = ['Push the button, show me something, and say: what is that, what logo is that, or what does that say.', 
               'Push the button,  and ask what is that, what logo is that, or what does that say.',
               'Push the button, show me something and say what is that, what logo is that, or what does that say.']
    rand_help = random.choice(helpArray)
    return rand_help
    
def random_hello():
    helloArray = ['hello  ' + (firstName) + '.       ' + random_help(), 
                'Hi  ' + (firstName) + '.         ' + random_help(), 
                'Welcome back ' + firstName + '.       ' + random_help(), 
                'Good to see you again,   '  + firstName + '.', 
                'Hi, ' + (firstName) + '      ' + 'nice to see you again.         ',
                'Hey, ' + (firstName) + '.     ' +  'great to see you again!        ']
    rand_hello = random.choice(helloArray)    
    return rand_hello

def random_welcome():
    welcomeArray = ['my pleasure', 'sure thing', 'you bet', 'you\'re welcome', 'no problem', 'no worries']
    rand_welcome = random.choice(welcomeArray)
    return rand_welcome
    
def random_goodbye():
    goodbyeArray = ['later dude', 'see ya later', 'later alligator', 'adios', 'ciao for now', 'so long', 'bye bye']
    rand_goodbye = random.choice(goodbyeArray)
    return rand_goodbye

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Vision & Speech Demo')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    
    hints = get_hints(args.language)
    
    client = CloudSpeechClient()
    
    #Greet the user
    tts.say(random_hello())
    
    with Board() as board:
        while True:
            board.led.state = Led.PULSE_SLOW
            
            if hints:
                logging.info('Push the button & show me something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Push the button & show me something.')
            
            board.button.wait_for_press()
            
            text = client.recognize(language_code=args.language, hint_phrases=hints)
            
            if text is None:
                logging.info('Sorry, what was that?')
            else:
                # Clear the output variable, so we don't repeat any previous results
                output = None
                quote = 0
                text = text.lower()
                
                logging.info('You said: "%s"' % text)
                
                if 'what is that' in text:
                    output = whatisthat.takeAndProcessImage('label')
                elif 'what is there' in text:
                    output = whatisthat.takeAndProcessImage('label')
                elif 'what\'s that' in text:
                    output = whatisthat.takeAndProcessImage('label')
                elif 'what logo is that' in text:
                    output = whatisthat.takeAndProcessImage('logo')
                elif 'what logo is there' in text:
                    output = whatisthat.takeAndProcessImage('logo')
                elif 'whose logo is that' in text:
                    output = whatisthat.takeAndProcessImage('logo')
                elif 'what does that say' in text:
                    output = whatisthat.takeAndProcessImage('text')
                    quote = 1
                elif 'can you read that' in text:
                    output = whatisthat.takeAndProcessImage('text')
                    quote = 1
                elif 'help' in text:
                    tts.say(random_help())
                elif 'thank you' in text:
                    tts.say(random_welcome())
                    break
                elif 'thanks' in text:
                    tts.say(random_welcome())
                    break
                elif 'well done' in text:
                    tts.say('no worries')
                    break
                elif 'great, thanks' in text:
                    tts.say(random_welcome())
                    break
                elif 'goodbye' in text:
                    tts.say(random_goodbye())
                    break
                elif 'so long' in text:
                    tts.say(random_goodbye())
                    break
                elif 'stop' in text:
                    tts.say(random_goodbye())
                    break
            
                # If we got a result then both print and speak it. 
                if output is not None:
                    if (quote == 1):
                        print(output)
                        tts.say(output)
                        tts.say('that\'s a quote by Albert Einstein')
                    #elif 'Dog' in output:
                        #tts.say('That\'s a Boston Terrier!')
                        #aiy.voice.audio.play_wav('/home/pi/AIY-projects-python/src/examples/voice/cloud-vision/wav/mono_dog.wav')
                    #elif 'Duck' in output:
                        #tts.say('That\'s a Mallard Duck!')
                        #aiy.voice.audio.play_wav('/home/pi/AIY-projects-python/src/examples/voice/cloud-vision/wav/mono_mallard.wav')
                    #elif 'Zebra' in output:
                        #tts.say('That\'s a Zebra!')
                        #aiy.voice.audio.play_wav('/home/pi/AIY-projects-python/src/examples/voice/cloud-vision/wav/mono_zebra.wav')
                    else:
                        print(output)
                        tts.say(output)
                else:
                    tts.say(random_error())
                    print("process failed")

if __name__ == '__main__':
    main()