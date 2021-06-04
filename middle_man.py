import xcffib
import xcffib.xproto
from xcffib.xproto import CW, EventMask, WindowClass, ConfigWindow
import config

class Atom_Cache():
    def __init__(self):
        self.__cache = {}

    def __getitem__(self, name):
        if name not in self.__cache:
            self.__cache[name] = mm.conn.core.InternAtom(False, len(name), name).reply().atom
        return self.__cache[name]

class Window():
    def __init__(self, wid):
        self.wid = wid # Window id of the window
        
    def get_property(self, prop, type):
        return mm.conn.core.GetProperty(
                False, 
                self.wid, 
                mm.atoms[prop],
                mm.atoms[type],
                0, 
                (2 ** 32) - 1
                ).reply().value

    def set_property(self, prop, type, value):
        if isinstance(value, str): 
            value = value.encode() # encode the string as utf8
            format = 8
        elif isinstance(value, list): 
            format = 32
        else:
            raise TypeError("value should be either a list of atoms or a string!")

        mm.conn.core.ChangeProperty(
                xcffib.xproto.PropMode.Replace,
                self.wid,
                mm.atoms[prop],
                mm.atoms[type],
                format,
                len(value),
                value
                )

    def get_attributes(self):
        return mm.conn.core.GetWindowAttributes(self.wid).reply()

    def set_attributes(self, value_mask, value_list):
        mm.conn.core.ChangeWindowAttributes(self.wid, value_mask, value_list)

    def configure(self, x=None, y=None, w=None, h=None, border_width=None, sibling=None, stack_mode=None, value_mask=None):
        value_list = []
        if value_mask is None:
            value_mask = 0
            if x is not None:
                value_mask |= ConfigWindow.X
                value_list.append(x)
            if y is not None:
                value_mask |= ConfigWindow.Y
                value_list.append(y)
            if w is not None:
                value_mask |= ConfigWindow.Width
                value_list.append(w)
            if h is not None:
                value_mask |= ConfigWindow.Height
                value_list.append(h)
            if border_width is not None:
                value_mask |= ConfigWindow.BorderWidth
                value_list.append(border_width)
            if sibling is not None:
                value_mask |= ConfigWindow.Sibling
                value_list.append(sibling)
            if stack_mode is not None:
                value_mask |= ConfigWindow.StackMode
                value_list.append(stack_mode)
        else:
            if value_mask & ConfigWindow.X: value_list.append(x)
            if value_mask & ConfigWindow.Y: value_list.append(y)
            if value_mask & ConfigWindow.Width: value_list.append(w)
            if value_mask & ConfigWindow.Height: value_list.append(h)
            if value_mask & ConfigWindow.BorderWidth: value_list.append(border_width)
            if value_mask & ConfigWindow.Sibling: value_list.append(sibling)
            if value_mask & ConfigWindow.StackMode: value_list.append(stack_mode)
        mm.conn.core.ConfigureWindow(self.wid, value_mask, value_list)

    def set_geometry(self, x=None, y=None, w=None, h=None):
        if x is not None: self.x = x
        if y is not None: self.y = y
        if w is not None: self.w = w
        if h is not None: self.h = h
        self.configure(x=self.x, y=self.y, w=self.w, h=self.h)

class Middle_Man():
    def __init__(self):
        self.conn = xcffib.Connection()
        self.setup = self.conn.setup
        self.screen = self.conn.get_screen_pointers()[0]
        self.root = Window(self.screen.root)
        self.atoms = Atom_Cache()

    # from https://rosettacode.org/wiki/Window_creation/X11#Python
    def create_window(self,x, y, w, h):
        wid = self.conn.generate_id()
        self.conn.core.CreateWindow(
                self.screen.root_depth,
                wid,
                self.root.wid,
                x,
                y,
                w,
                h,
                0,
                WindowClass.InputOutput,
                self.screen.root_visual,
                CW.BackPixel | CW.EventMask,
                [self.screen.white_pixel, EventMask.StructureNotify | EventMask.Exposure]
                )
        return Window(wid)

    def become_wm(self):
        # Check if another wm is already running
        supporting_wid = self.root.get_property("_NET_SUPPORTING_WM_CHECK", "WINDOW").to_atoms()
        if len(supporting_wid) > 0:
            supporting_wid = supporting_wid[0]
            supporting_win = Window(supporting_wid)
            existing_wmname = supporting_win.get_property("_NET_WM_NAME", "UTF8_STRING").to_string()
            if existing_wmname:
                raise Exception("Another window manager ({}) is running.".format(existing_wmname))

        # Make a window for wm check
        supporting_win = self.create_window(-1, -1, 1, 1)
        supporting_win.set_property("_NET_SUPPORTING_WM_CHECK", "WINDOW",      [supporting_win.wid])
        supporting_win.set_property("_NET_WM_NAME",             "UTF8_STRING", config.name)
        self.root.set_property(     "_NET_SUPPORTING_WM_CHECK", "WINDOW",      [supporting_win.wid])

        # Sets the supported atoms from the ewmh extension
        # https://en.wikipedia.org/wiki/Extended_Window_Manager_Hints
        self.root.set_property("_NET_SUPPORTED", "ATOM", [self.atoms[prop] for prop in [
            "_NET_SUPPORTED",
            "_NET_SUPPORTING_WM_CHECK",
            "_NET_WM_NAME",
            ]])

        # Selects the events we want to listen to
        # All the possible events are listed but I commented the ones I dont want to respond to
        self.root.set_attributes(CW.EventMask, [
            #EventMask.NoEvent |
            #EventMask.KeyPress |
            #EventMask.KeyRelease |
            #EventMask.ButtonPress |
            #EventMask.ButtonRelease |
            EventMask.EnterWindow |
            EventMask.LeaveWindow |
            #EventMask.PointerMotion |
            #EventMask.PointerMotionHint |
            #EventMask.Button1Motion |
            #EventMask.Button2Motion |
            #EventMask.Button3Motion |
            #EventMask.Button4Motion |
            #EventMask.Button5Motion |
            #EventMask.ButtonMotion |
            #EventMask.KeymapState |
            EventMask.Exposure |
            EventMask.VisibilityChange |
            EventMask.StructureNotify |
            EventMask.ResizeRedirect |
            #EventMask.SubstructureNotify |
            EventMask.SubstructureRedirect |
            #EventMask.FocusChange |
            #EventMask.PropertyChange |
            #EventMask.ColorMapChange |
            #EventMask.OwnerGrabButton |
            0 # Zero at the end so you can comment and uncomment without worrying about the pipes
        ])
        self.conn.flush()

    def run(self):
        while True:
            event = self.conn.wait_for_event()
            if False: pass # So you can comment and move stuff around 
            elif isinstance(event, xcffib.xproto.ConfigureRequestEvent): self.__event_configure_request(event)
            elif isinstance(event, xcffib.xproto.MapRequestEvent): self.__event_map_request(event)
            elif isinstance(event, xcffib.xproto.DestroyNotifyEvent): self.__event_destroy_notify(event)
            else: print(type(event))
            self.conn.flush()

    def __event_configure_request(self, event):
        Window(event.window).configure(event.x, event.y, event.width, event.height, event.border_width, event.sibling, event.stack_mode, event.value_mask)

    def __event_map_request(self, event):
        win = Window(event.window)
        if win.get_attributes().override_redirect: return
        self.conn.core.MapWindow(event.window)
    
    def __event_destroy_notify(self, event):
        pass

mm = Middle_Man()
mm.become_wm()
