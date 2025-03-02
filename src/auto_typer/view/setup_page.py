from flet import Page
def page_and_window_setup(page:Page):
    page.title = "AutoTyper"
    page.window.icon = "./icon.png"
    page.window.width = 800
    page.window.height = 950  
    page.window.always_on_top = True
    page.window.resizable = False
    page.window.center()
    page.window.visible = True
    page.update()