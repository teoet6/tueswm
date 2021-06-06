from middle_man import mm, Bind
import xcffib.xproto
from xcffib.xproto import ModMask, ButtonMask, EventMask, GrabMode, Cursor, Time

class Manager():
    def __init__(self):
        pass

    def on_window_created(self, wid):
        pass

    # You can't use mm.windows[wid] here because the window is destroyed!!
    def on_window_destroyed(self, wid):
        pass

    def on_window_changed(self, wid):
        pass

class Default_Manager(Manager):
    def __init__(self):
        self.button_binds = [
            Bind(ModMask._4, 1, self.mousemove),
            Bind(ModMask._4, 2, self.resize, [500, 500]),
            Bind(ModMask._4, 3, self.mouseresize),
        ]

    def on_window_created(self, wid):
        pass

    def on_window_destroyed(self, wid):
        pass

    def on_window_changed(self, wid):
        pass

    def mousemove(self, wid):
        if wid == mm.root.wid: return
        # TODO Abstract GrabPinter and UngrabPointer away
        mm.conn.core.GrabPointer(False, wid, EventMask.PointerMotion | EventMask.ButtonPress | EventMask.ButtonRelease, GrabMode.Async, GrabMode.Async, 0, Cursor._None, Time.CurrentTime, is_checked=True)
        mm.conn.flush()

        pointer_pos = mm.conn.core.QueryPointer(wid).reply()
        dx = pointer_pos.root_x - mm.windows[wid].x 
        dy = pointer_pos.root_y - mm.windows[wid].y 

        while True:
            event = mm.wait_for_event()
            if isinstance(event, xcffib.xproto.ButtonPressEvent): break
            if isinstance(event, xcffib.xproto.ButtonReleaseEvent): break
            if isinstance(event, xcffib.xproto.MotionNotifyEvent): 
                mm.windows[wid].configure(event.root_x - dx, event.root_y - dy)
            else: mm.handle_event(event)
            mm.conn.flush()
        mm.conn.core.UngrabPointer(Time.CurrentTime)
        mm.conn.flush()

    def resize(self, wid, w, h):
        pass

    def mouseresize(self, wid):
        if wid == mm.root.wid: return
        # TODO Abstract GrabPinter and UngrabPointer away
        mm.conn.core.GrabPointer(False, wid, EventMask.PointerMotion | EventMask.ButtonPress | EventMask.ButtonRelease, GrabMode.Async, GrabMode.Async, 0, Cursor._None, Time.CurrentTime, is_checked=True)
        mm.conn.flush()

        while True:
            event = mm.conn.wait_for_event()
            if isinstance(event, xcffib.xproto.ButtonPressEvent): break
            if isinstance(event, xcffib.xproto.ButtonReleaseEvent): break
            if isinstance(event, xcffib.xproto.MotionNotifyEvent): 
                mm.windows[wid].configure(None, None, max(30, event.root_x - mm.windows[wid].x), max(30, event.root_y - mm.windows[wid].y))
            else: mm.handle_event(event)
            mm.conn.flush()
        mm.conn.core.UngrabPointer(Time.CurrentTime)
        mm.conn.flush()
