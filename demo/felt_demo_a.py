import flet as ft


def main(page: ft.Page):
    page.title = "A Flet Demo"
    page.window.width = 275
    page.window.height = 100
    page.add(ft.Text("Hello there... stay a while and listen!"))

ft.app(main)