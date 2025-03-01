import flet as ft
from classes.window import TargetWindow
from classes.data import TextData
from classes.typer import Typer
from classes.components import AppCoverAlert



class AppState:

    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppState, cls).__new__(cls)
        return cls.instance

    def __init__(self, page:ft.Page=None):
        self.title = "AutoTyper"
        self.icon = "./icon.png"
        self.width = 800
        self.height = 950
        self.always_on_top = True
        self.resizable = True

        # Flet GUI Objects
        if not page:
            self.page = None
            self.window = None
        else:
            self.page: ft.Page = page
            self.window = page.window

        # Target Window
        self.target_window = None
        self.target_window_title = None
        self.set_hotkeys = None
        
        # Text Data
        self.source_file_path = None
        self.text_data = None

        # Typer Settings
        self.typer= None
        self.speed = 100
        self.play = False
        self.paused = False
        self.pause_on_new_line = False
        self.advance_to_newline = 0
        self.advance_token = 0
        self.start_playback_paused = False

        # Explosed GUI functions
        self.pause_playback = None # function
        self.tokens_preview = None # textbox
        self.tokens_preview_list = None # list

        # Thread variables
        self.hotkeys = []
        self.close = False

    def get_target_window(self):
        if self.page:        
            alert = AppCoverAlert(
                page=self.page,
                text="please click on the target application now",
                action=TargetWindow,
                display_time=0
            )
            self.target_window = alert.action_result
            return self.target_window.parent_title
        
    def initialize_text_data(self, file_path):
        try:
            with open(file_path,'r') as f:
                file_data = f.read()
                self.text_data = TextData(file_data)
                self.tokens_preview_list = ['[ ' + str(x) + ' ]' for x in self.text_data.text_tokens]
                self.tokens_preview.current.value = " ".join(self.tokens_preview_list)
                self.page.update()
                

        except Exception as e:
            if self.page:        
                AppCoverAlert(page=self.page, text=f"{e}.", bgcolor="#FFCCCB", color="white", icon=ft.Icon(name=ft.Icons.ERROR))

    def initalize_typer(self):
        if self.text_data:
            self.typer = Typer(
                text_tokens=self.text_data.text_tokens,
                speed=self.speed,
                pause_on_new_line=self.pause_on_new_line,
                window_title=self.target_window_title,
                play=self.play,
                paused=self.paused,
                pause_on_window_not_focused=True,
                start_playback_paused = self.start_playback_paused,
                app_state=self
            )

    def update_tokens_preview(self):
        self.tokens_preview_list.pop(0)
        self.tokens_preview.current.value = " ".join(self.tokens_preview_list)
        self.page.update()

        

