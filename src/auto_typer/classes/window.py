from classes.mouse import MousePointer

class TargetWindow:
    def __init__(self):
        mp = MousePointer()
        parent_hwnd, child_hwnd, window_title = mp.clicked_on()
        self._hwnd = parent_hwnd
        self._child_hwnd = child_hwnd
        self._window_title = window_title

    @property
    def hwnd(self):
        return self.hwnd
    
    @property
    def child_hwnd(self):
        return self._child_hwnd
    
    @property
    def parent_title(self):
        return self._window_title 