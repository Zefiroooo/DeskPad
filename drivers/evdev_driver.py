import evdev
import time
from evdev import ecodes, UInput, InputDevice
from drivers.base import BaseInputController

class EvdevDriver(BaseInputController):
    def __init__(self):
        capabilities = {
            ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y, ecodes.REL_WHEEL],
            ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT]
        }

        self.ui = UInput(capabilities, "Virtual Mouse")

    def move(self, dx, dy):
        self.ui.write(ecodes.EV_REL, ecodes.REL_X, int(dx))
        self.ui.write(ecodes.EV_REL, ecodes.REL_Y, int(dy))
        self.ui.syn()

    def scroll(self, dy):
        self.ui.write(ecodes.EV_REL, ecodes.REL_WHEEL, int(dy))
        self.ui.syn()
        pass

    def click(self, button):
        
        pass

    def close(self):
        self.ui.close()



