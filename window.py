from config import conn
import xcffib
# Returns the atom for any atom name.
def get_atom(conn, name):
    return conn.core.InternAtom(False, len(name), name).reply().atom
xcffib.Connection.get_atom = get_atom
# Calling conn.get_atom(...) is the same as get_atom(conn ...). It's just more python-y this way

import xcffib.xproto
ConfigWindow = xcffib.xproto.ConfigWindow

class Window():
    def __init__(self, wid):
        self.wid = wid # Window id of the window
        geom = conn.core.GetGeometry(wid).reply()
        self.x = geom.x
        self.y = geom.y
        self.w = geom.width
        self.h = geom.height
        
    def get_property(self, prop, type):
        return conn.core.GetProperty(
                False, 
                self.wid, 
                conn.get_atom(prop),
                conn.get_atom(type),
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

        conn.core.ChangeProperty(
                xcffib.xproto.PropMode.Replace,
                self.wid,
                conn.get_atom(prop),
                conn.get_atom(type),
                format,
                len(value),
                value
                )

    def get_attributes(self):
        return conn.core.GetWindowAttributes(self.wid).reply()

    def set_attributes(self, value_mask, value_list):
        conn.core.ChangeWindowAttributes(self.wid, value_mask, value_list)

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
        conn.core.ConfigureWindow(self.wid, value_mask, value_list)

    def set_geometry(self, x=None, y=None, w=None, h=None):
        if x is not None: self.x = x
        if y is not None: self.y = y
        if w is not None: self.w = w
        if h is not None: self.h = h
        self.configure(x=self.x, y=self.y, w=self.w, h=self.h)
