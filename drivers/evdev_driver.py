import evdev
import time
from evdev import ecodes, UInput, InputDevice
from drivers.base import BaseInputController

class EvdevDriver(BaseInputController):
    def __init__(self):
        capabilities = {
            ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y, ecodes.REL_WHEEL],
            ecodes.EV_KEY: [
                ecodes.BTN_LEFT, ecodes.BTN_RIGHT, ecodes.KEY_LEFT, ecodes.KEY_RIGHT, ecodes.KEY_ESC,
                ecodes.KEY_LEFTALT, ecodes.KEY_LEFTCTRL, ecodes.KEY_P, ecodes.KEY_F5
            ]
            }
        
        self.KEY_MAPPING : dict = {
            "next" : [ecodes.KEY_RIGHT],
            "prev" : [ecodes.KEY_LEFT],
            "exit" : [ecodes.KEY_ESC],
            "black": [ecodes.KEY_B],

            "start_ppt" : [ecodes.KEY_F5],
            "start_canva" : [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTALT, ecodes.KEY_P]
        }

        self.ui = UInput(capabilities, "Virtual Mouse")

    def move(self, dx, dy):
        self.ui.write(ecodes.EV_REL, ecodes.REL_X, int(dx))
        self.ui.write(ecodes.EV_REL, ecodes.REL_Y, int(dy))
        self.ui.syn()

    def scroll(self, dy):
        self.ui.write(ecodes.EV_REL, ecodes.REL_WHEEL, int(dy))
        self.ui.syn()

    def click(self, button, action: str = "click"):
        if button == "right":
            if action == "down":
                self.ui.write(ecodes.EV_KEY, ecodes.BTN_RIGHT, 1)
                self.ui.syn()
            elif action == "up":
                self.ui.write(ecodes.EV_KEY, ecodes.BTN_RIGHT, 0)
                self.ui.syn()

        elif button == "left":
            if action == "down":
                self.ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 1)
                self.ui.syn()
            elif action == "up":
                self.ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 0)
                self.ui.syn()


    def key_press(self, key_name: str):
        keys = self.KEY_MAPPING.get(key_name)
        if not keys : return

        for k in keys:
            self.ui.write(ecodes.EV_KEY, k, 1)
        self.ui.syn()

        for k in keys:
            self.ui.write(ecodes.EV_KEY, k, 0)
        self.ui.syn()
    

    def close(self):
        self.ui.close()



