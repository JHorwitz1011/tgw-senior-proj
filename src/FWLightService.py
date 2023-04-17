# python 3.6

import time
import json
import neopixel
import board
import csv
import math
from paho.mqtt import client as mqtt_client

import sys
import os
# sys.path.append(os.path.expanduser('$HOME/templates'))
from MQTTObject import MQTTObject

from LightConstants import *

class FWLightService(MQTTObject):
    """Handles animatinos at a constant FPS. For more information, see LightConstants.py and MQTTObject.py"""

    def __init__(self, pin=PIN, fs=DEFAULT_SAMPLING_RATE):
        super().__init__()
        #topics and callbacks for superclass
        self.callbacks = {
            LIGHTBAR_TOPIC : self.on_lightbar_message,
            MAINLED_TOPIC :  self.on_buttonled_message
        }

        #lightbar speccific objects 
        self.pixels = neopixel.NeoPixel(pin, NUM_LEDS)
        self.animation_queue = []
        self.empty = True
        self.fs = fs
        
        
        # button LED related constants
        self.indicatorColor = (255,255,255)
        self.indicatorAnimation = 'pulse'


    def on_lightbar_message(self, client, userdata, msg):
        """
        Lightbar callback
        """
        payload = json.loads(msg.payload)
        try:
            payload_type = payload['data']['type'] 
            if payload_type == 'animation':
                self.empty = False
                print(f'animation received. {payload["data"]["animation"]}')
                self.animation_queue.append(self._grab_animation_from_csv(animation_codes[payload['data']['animation']]))
            elif payload_type == 'raw':
                self.update_strip(payload['data']['raw'])
        except KeyError as e:
            print("ERROR: Invalid Animation", e)

    def on_buttonled_message(self, client, userdata, msg):
        """
        Button callback
        """
        
        payload = json.loads(msg.payload)
        try:
            self.pixels[0] = tuple(payload["data"]["color1"])
        except KeyError:
            print("ERROR: Invalid Animation")

    def run(self):
        """
        Starts MQTT client and begins listening for frames to push to lights
        """
        self.start_mqtt(LIGHTS_CLIENT_ID, self.callbacks)
        
        while True:
            if self.animation_queue:
                self.empty = False
                try:
                    animation = self.animation_queue.pop(0)
                    self.animate_blocking(animation[1], animation[0])
                    print(f"playing animation {animation}")
                except:
                    print("ERROR: frame not played")
            elif not self.empty:
                self.current_frame = EMPTY_LIGHTS
                self.update_strip(EMPTY_LIGHTS)
                self.empty=True
                print('empty!')




    ################# LIGHT HANDLING ######################
    def animate_blocking(self, colordata, lengthdata):
        for x in range(len(colordata)):
            self.current_frame = colordata[x]
            self.update_strip(colordata[x])
            time.sleep(lengthdata[x])

    def update_strip(self, display_frame):
        for x in range(len(display_frame)):
            self.pixels[display_to_hardware_adapter[x]] = display_frame[x]
        self.pixels.show()

    def _grab_animation_from_csv(self, filepath):
        animation = []
        color = []
        lengths = []
        try:
            file = open(filepath, newline='')
            for row in csv.reader(file, delimiter=',', quotechar='|'):
                animation.append(row)

            for a in animation:
                lengths.append(float(a[0])/1000)
            for a in animation:
                color.append(a[1:])
            for data in color:
                for index in range(len(data)):
                    data[index] = int(data[index][1:], 16)
        except KeyError:
            print(f"ERROR: {filepath} not found")
        return lengths, color


if __name__ == '__main__':
    service = FWLightService()  
    service.run() 