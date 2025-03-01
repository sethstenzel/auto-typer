import win32gui
from pynput import mouse
from pynput.mouse import Button

class MousePointer:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MousePointer, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.listener = None
        self.last_clicked_on = None

    def get_window_at(self, x, y):
        captured_hwnd = win32gui.WindowFromPoint((x, y))
        parent_window_title = None
        parent_hwnd = {
            "parent_hwnd": None,
            "child_hwnd": None,
            "window_title": None
        }
        def match_hwnd(new_hwnd, _):
            if win32gui.IsWindowVisible(new_hwnd):
                
                children_hwnds = []
                def enum_children(hwnd, param):
                    children_hwnds.append(hwnd)      
                
                win32gui.EnumChildWindows(new_hwnd, enum_children, None)

                if captured_hwnd in children_hwnds or captured_hwnd == new_hwnd:
                    nonlocal parent_window_title, parent_hwnd
                    parent_hwnd = new_hwnd
                    parent_window_title = win32gui.GetWindowText( new_hwnd )

        win32gui.EnumWindows( match_hwnd , None )
        
        return parent_hwnd, captured_hwnd, parent_window_title

    @staticmethod
    def on_mouse_click(x, y, button, pressed):
        mp:MousePointer = MousePointer.instance
        if pressed and button == Button.left:
            parent_hwnd, captured_hwnd, parent_window_title = mp.get_window_at(x, y)
            if parent_window_title and parent_window_title != "":
                mp.last_clicked_on = (parent_hwnd, captured_hwnd, parent_window_title)
                if mp.listener:
                    mp.listener.stop()
  
    def clicked_on(self):
        self.listener = mouse.Listener(on_click=self.on_mouse_click)
        self.listener.start()
        self.listener.join()
        return self.last_clicked_on

if __name__ == "__main__":
    mp = MousePointer()
    clicked_window = mp.clicked_on()
    print(f"Clicked on Window: {clicked_window}")


