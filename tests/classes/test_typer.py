from auto_typer.classes.typer import Typer
from auto_typer.classes.data import TextData
import tkinter as tk
import threading

import clipboard as cb
import time

def test_type_text_tokens_with_gui_app():
    def create_tk_test_window():
        root = tk.Tk()
        root.title("AutoTyperTestWindow")
        root.geometry("340x220")
        root.lift()        
        text_box = tk.Text(root, wrap=tk.WORD)
        text_box.pack(fill=tk.BOTH, expand=True)

        def copy_text(event):
            try:
                cb.copy(text_box.get('1.0', tk.END).rstrip('\n'))
            except tk.TclError as e:
                pass

        def close_app(event=None):
            root.destroy()

        def on_focus_in(event):
            text_box.focus_set()

        text_box.bind('<Control-c>', copy_text)
        text_box.bind('<Control-e>', close_app)
        root.bind("<FocusIn>", on_focus_in)

        root.after(60000, close_app)
        root.mainloop()
    mock_source_file_data = """import flet as ft
from classes.app_state import AppState


def main(page: ft.Page):
    app_state = AppState(page)
    page.title = app_state.title
   
    page.window.center()
    page.update()"""
    gui_control_commands = "<<ctrl+c>><<pause=2>><<ctrl+e>>"
        
    test_data = TextData(text_to_type=mock_source_file_data+gui_control_commands)
    typer = Typer(
        text_tokens = test_data.text_tokens,
        play = True,
        paused = False,
        speed = 100,
        pause_on_new_line = True,
        window_title = "AutoTyperTestWindow",
        pause_on_window_not_focused = True
    )
    tk_win_thread = threading.Thread(target=create_tk_test_window, args=())
    tk_win_thread.start()
    time.sleep(5)
    typer.type_text_tokens()
    clipboard_contents = cb.paste()
    assert clipboard_contents == mock_source_file_data


