import xcffib
import xcffib.xproto
from connection import Connection

conn = xcffib.Connection() # The connection to the X11 server
screen = conn.get_screen_pointers()[0] # The first screen from the server. SCREEN AND MONITOR ARE NOT THE SAME TERMS!
name = "tueswm" # The name of the window manager
border_width = 10; # Width of window borders

class Bind():
    def __init__(self, mods, key, on_trigger):
        self.mods = mods
        self.key = key
        self.on_trigger

#key_binds = [
#    Bind()
#]
