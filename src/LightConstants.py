import board
import neopixel

VERSION = 1.0
TYPE = 'UI_LIGHTBAR'

BROKER = 'localhost'
PORT = 1883
LIGHTBAR_TOPIC = "goodwand/ui/view/lightbar"
MAINLED_TOPIC = "goodwand/ui/view/main_led"

LIGHTS_CLIENT_ID = 'TGWLightService'
NUM_LEDS = 21
PIN = board.D12
ORDER = neopixel.GRB
DEFAULT_SAMPLING_RATE = 30 #hz

animation_codes = {
    "yipee": "yipee.csv",
    "yes": "yes_confirmed.csv",
    "no": "no_failed.csv",
    "confused": "confused_not_understood.csv",
    "up_down": "green_up_down.csv"
}

EMPTY_LIGHTS = [(0,0,0)]*20

display_to_hardware_adapter = {
        0:1,
        1:20,
        2:2,
        3:19,
        4:3,
        5:18,
        6:4,
        7:17,
        8:5,
        9:16,
        10:6,
        11:15,
        12:7,
        13:14,
        14:8,
        15:13,
        16:9,
        17:12,
        18:10,
        19:11,
    }