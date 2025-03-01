import time
from  .data import SingleKey, MultiKeys, TimedPause, MouseScroll
from pynput.keyboard import Key, Controller as KbController
from pynput.mouse import Controller as MsController
import pygetwindow as gw
import win32gui, win32com.client
import pythoncom
import flet as ft
from .components import AppCoverAlert

class Typer:
    def __init__(self,
        *,
        text_tokens = None,
        play:bool = True,
        paused:bool = False,
        speed:int = 100,
        pause_on_new_line:bool = True,
        window_title:str = "AutoTyperTestWindow",
        pause_on_window_not_focused:bool = True,
        start_playback_paused = False,
        app_state = None,
        auto_home_on_newline = False,
        control_on_newline = False
    ):
        self.text_tokens = text_tokens
        self.play = play
        self.paused = paused
        self.speed = speed
        self.pause_on_new_line = pause_on_new_line
        self.window_title = window_title
        self.pause_on_window_not_focused = pause_on_window_not_focused
        self.start_playback_paused = start_playback_paused
        self.app_state = app_state
        self.auto_home_on_newline = auto_home_on_newline
        self.control_on_newline = control_on_newline
        self.advance_to_newline = 0
        self.advance_token = 0
        self.hwnd = None
        self.kb = KbController()
        self.ms = MsController()


    def type_token(self, token):
        kb = self.kb
        ms = self.ms
        token_completed = False
        
        while not token_completed and self.play:
            if isinstance(token, MultiKeys):
                if self.check_window_focused(pause_if_not=True):
                    for key in token.keys:
                        self.focus_window()
                        if hasattr(Key, key):
                            kb.press(getattr(Key, key))
                        else:
                            kb.press(key)
                    time.sleep(self.speed/1000/2)
                    for key in token.keys:
                        self.focus_window()
                        if hasattr(Key, key):
                            kb.release(getattr(Key, key))
                        else:
                            kb.release(key)
                    token_completed = True
            elif isinstance(token, SingleKey):
                if self.check_window_focused(pause_if_not=True):
                    if token.key == "enter" and self.control_on_newline:
                        kb.press(Key.ctrl)
                        kb.press(getattr(Key, token.key))
                        time.sleep(self.speed/1000)
                        kb.release(getattr(Key, token.key))
                        kb.release(Key.ctrl)
                    else:
                        kb.press(getattr(Key, token.key))
                        time.sleep(self.speed/1000)
                        kb.release(getattr(Key, token.key))
                        
                    if token.key == "enter" and self.auto_home_on_newline:
                        kb.press(Key.home)
                        time.sleep(self.speed/1000)
                        kb.release(Key.home)

                    if (token.key == "enter" and self.app_state.pause_on_new_line) or (token.key == "enter" and self.advance_to_newline > 0):
                        if self.advance_to_newline > 0:
                            self.advance_to_newline -= 1
                        self.paused = True
                        self.app_state.paused = True
                    token_completed = True


            elif isinstance(token, TimedPause):
                if self.check_window_focused(pause_if_not=True):
                    time.sleep(token.time)
                    token_completed = True
            elif isinstance(token, MouseScroll):
                if self.check_window_focused(pause_if_not=True):
                    for _ in range(token.scroll_count):
                        ms.scroll(0, token.scroll_direction)
                        time.sleep(self.speed/1000/2)
                    token_completed = True
            else:
                for char in token:
                    char_completed = False
                    while not char_completed:
                        if (
                            (self.check_window_focused(pause_if_not=True) and not self.paused) or
                            (self.play and self.paused and self.advance_to_newline > 0) or
                            (self.play and self.paused and self.advance_token > 0)
                        ):  
                            self.focus_window()
                            kb.press(char)
                            time.sleep(self.speed/1000)
                            kb.release(char)
                            char_completed = True
                        time.sleep(0.01)
                token_completed = True
        time.sleep(0.01)
        return token_completed


    def type_text_tokens(self):
        self.focus_window()
        if self.start_playback_paused:
            self.app_state.paused = True
            self.paused=True
        for token in self.text_tokens:
            token_completed = False
            while not token_completed and self.play is True: 
                if (
                    (self.play and not self.paused) or
                    (self.play and self.paused and self.advance_to_newline > 0) or
                    (self.play and self.paused and self.advance_token > 0)
                ):  
                    if (not self.paused and self.check_window_focused(pause_if_not=True) or
                        (self.play and self.paused and self.advance_to_newline > 0) or
                        (self.play and self.paused and self.advance_token > 0)
                    ):  
                        self.focus_window()
                        token_completed = self.type_token(token)
                        if token_completed and self.advance_token > 0:
                            self.advance_token -= 1
                if not self.play:
                    break
                if self.paused:
                    time.sleep(0.1)
            if not self.play:
                break
            if token_completed:
                if self.app_state:
                    self.app_state.update_tokens_preview()
                    
                


    def focus_window(self):
        pythoncom.CoInitialize()
        if not self.check_window_focused():
            try:
                if not self.hwnd:
                    hwnd = win32gui.FindWindow(None, self.window_title)
                    if hwnd == 0:
                        raise ValueError(f"Unable to locate window:\n{self.window_title}")
                    self.hwnd = hwnd

                if self.hwnd:
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shell.SendKeys('%')
                    win32gui.SetForegroundWindow(self.hwnd)
            except Exception as e:
                self.play = False
                AppCoverAlert(
                    display_time=6,
                    page=self.app_state.page,
                    text=str(e),
                    bgcolor="#FFCCCB",
                    color="white",
                    icon=ft.Icon(name=ft.Icons.ERROR))
            time.sleep(0.25)

    
    def check_window_focused(self, pause_if_not = False):
        active_window = gw.getActiveWindow()
        if not active_window or active_window._hWnd != self.hwnd:
            if pause_if_not:
                self.paused = True
                self.app_state.paused = True
            return False
        return True
