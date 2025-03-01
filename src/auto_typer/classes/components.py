import flet as ft
import time 

class AppCoverAlert:
    def __init__(self, *, page=None, text=None, color=None, bgcolor=None, action=None, display_time=3, icon=None):
        self.page = page
        self.text = text
        self.color = color
        self.bgcolor = bgcolor
        self.action = action
        self.display_time = display_time
        self.action_result = None
        self.icon = icon
        self.show()

    def show(self):
        if self.page and self.text:
            dialog = ft.AlertDialog()
            if self.icon:
                dialog.icon=self.icon or ft.Icon(name=ft.Icons.INFO)
            if self.color:
                dialog.title=ft.Text(self.text, color=self.color)
            else:
                dialog.title=ft.Text(self.text)
            if self.bgcolor:
                dialog.bgcolor=self.bgcolor
            if self.page:
                self.page.open(dialog)
                if self.action:
                    self.action_result = self.action()
                if self.display_time > 0:
                    time.sleep(self.display_time)
                self.page.close(dialog)     