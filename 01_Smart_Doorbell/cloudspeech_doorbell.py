#!/usr/bin/env python3

# Author: Liz Myers | https://www.linkedin.com/in/lizmyers/
# Tutorial: https://www.hackster.io/publishedLinkGoesHere

# REQURIRED: this script requires your unique Google Cloud Credentials
# Insert them on lines 58-62 and uncomment line 136 to upload photos

# REOMMENDED: Add your own sound files. Mono files in .WAV format work best.
# A good resource for sound effects is https://www.soundrangers.com

"""A prototype smart doorbell - using Google Cloud Services"""

import argparse
import locale
import logging
import io
import os
import aiy
import picamera

# required for the camrea LED
import RPi.GPIO as GPIO

# python wrapper for easy image upload
import pyrebase

from aiy.voice import tts
from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient
from aiy.voice.audio import AudioFormat, play_wav
from picamera import PiCamera
from time import sleep

language = 'en'

def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('turn on the light',
                'turn off the light',
                'blink the light',
                'goodbye')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language
    
def takePhoto():
    with picamera.PiCamera () as camera:
        camera.resolution = (640, 480)
        camera.rotation = 180
        camera.ISO = 400
        camera.brightness = 55
        camera.contrast = 60
        camera.capture('/home/pi/AIY-projects-python/src/examples/voice/doorbell/doorbell.jpg')
        return None
        
def uploadImg():
        config = {
            "apiKey": "1:012345678901:android:abcde12345fghij6",
            "authDomain": "doorbell-123456.firebaseapp.com",
            "databaseURL": "https://doorbell-123456.firebaseio.com",
            "storageBucket": "doorbell-123456.appspot.com",
            "serviceAccount": "/home/pi/doorbell-service-account.json"
        }
        firebase = pyrebase.initialize_app(config)
        print('config done')

        storage = firebase.storage()
        storage.child("doorbell.jpg").put("doorbell.jpg")
        print('Success! A new photo, doorbell.jpg, was uploaded to google cloud.')
        return None

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Adding Vision to the Voice Kit.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()
    
    #Controls Servo (row 0) GPIO on Voice Hat
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26,GPIO.OUT)

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()

    with Board() as board:
        while True:
            logging.info('Please ring the doorbell.')
            
            #Pulse the Arcade button to show it's active
            board.led.state = Led.PULSE_QUICK
            board.button.wait_for_press()
            
            #Add you own doorbell sound and uncomment the next line
            #aiy.voice.audio.play_wav('/home/pi/AIY-projects-python/src/examples/voice/doorbell/<your_mono_soundFile.wav>')
            
            #We don't need the button any more, turn the light off to focus attention on the camera
            board.led.state = Led.OFF
            tts.say('Welcome! Let me take your picture.')
            
            #Turning the red LED on to draw attention and indicate the camera is activated
            GPIO.output(26,GPIO.HIGH)
            
            tts.say('Ready? Here we go, in 3, 2, 1')
            takePhoto()
            
            #Adding a 'camera-click' sound, confirms the picture has been taken. 
            #Please ADD YOUR own 'click' sound and uncomment the next line.
            #aiy.voice.audio.play_wav('/home/pi/AIY-projects-python/src/examples/voice/doorbell/your_mono_soundFile.wav')
            
            #Camera is done - so turn off the red LED
            GPIO.output(26,GPIO.LOW)
            
            tts.say('Nice! Hang on while we check your I.D.')
            #wait a few seconds (simulating face recognition)
            sleep(3)
            
            #SUCCESS
            #Turn the (green) Arcade LED back on to signal the user can GO inside
            #If your Arcade button is not green, perhaps substitute a neopixel ring here
            board.led.state = Led.ON
            
            #Add a 'success' sound and uncomment the next line.
            #aiy.voice.audio.play_wav('/home/pi/AIY-projects-python/src/examples/voice/doorbell/your_mono_soundFile.wav')
            
            #Insert your name here: 'Okay, <YOUR-FIRST-NAME>, it looks like you. Please come in!'
            tts.say('Okay, it looks like you. Please come in!')
            
            #Add a 'door-opening' sound and uncomment the next line
            #aiy.voice.audio.play_wav('/home/pi/AIY-projects-python/src/examples/voice/doorbell/your_mono_soundFile.wav')
            
            #IMPORTANT - add YOUR login credentials to the config section (line 69)
            # and uncomment the next line
            #uploadImg()
            
            logging.info('Smart Doorbell script complete!')
            
            break

if __name__ == '__main__':
    main()