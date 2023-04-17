import time
import json
import signal

import sys
import os
sys.path.append(os.path.expanduser('~/templates'))
from MQTTObject import MQTTObject

KEYWORD_TOPIC = "goodwand/ui/controller/keyword"
LIGHT_TOPIC = "goodwand/ui/view/lightbar"
GENERIC_CLIENT_ID = "light-show"

COLOR_PRESETS = {
    'white': 20*[(255, 255, 255)],
    'purple': 20*[(160, 32, 240)],
    'blue': 20*[(0, 0, 255)],
    'black': 20*[(0,0,0)],
    'grey': 20*[(10,10,10)],
    'orange': 20*[(255, 165, 0)],
    'green': 20*[(0,255,0)],
    'red':20*[(255, 0, 0)],
    'yellow': 20*[(255,255,0)],
    'brown': 20*[(0,0,0)],
    'noise': 20*[(0,0,0)]
}

MINIMUM_THRESHOLD = 0.7

PKT_TEMPLATE = pkt = {
    "header": {
        "type": "UI_LIGHTBAR",
        "version": 1,
    },
    "data": {
        "type": 'raw',
        "raw": None,
    }
}

class GenericMQTTService(MQTTObject):

    def __init__(self):
        super().__init__()

        self.callbacks = {
            KEYWORD_TOPIC : self.keyword_callback,
        }

    def keyword_callback(self, client, userdata, msg):
        payload = json.loads(msg.payload)
        for color in payload['data'].keys():
            if color != 'noise' and color != 'brown' and payload['data'][color] > MINIMUM_THRESHOLD:
                PKT_TEMPLATE['data']['raw'] = COLOR_PRESETS[color]
                self.publish(LIGHT_TOPIC, json.dumps(PKT_TEMPLATE))
            

    def run(self):
        self.start_mqtt(GENERIC_CLIENT_ID, self.callbacks)
        signal.pause()


if __name__ == '__main__':
    service = GenericMQTTService()  
    service.run() 