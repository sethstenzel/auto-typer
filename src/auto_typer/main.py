import flet as ft
import time
from classes.app_state import AppState
import threading
from view.page_setup import page_and_window_setup


def main(page: ft.Page):
    app_state = AppState(page)
    page_and_window_setup(page) 

    ############################## WINDOW SETTINGS ##############################


    ############################## FUNCTIONS ##############################
    def select_target_app_btn_clk(e):
        target_application_title = app_state.get_target_window()
        app_state.target_window_title = target_application_title
        nonlocal target_application_title_text
        target_application_title_text.current.value = target_application_title
        page.update()
        check_enable_start()


    def update_slider_label(e):
        typing_speed_label.current.value = f"auto typing Speed: {int(typing_speed.current.value)} ms"
        if app_state:
            app_state.speed = int(typing_speed.current.value)
        if app_state.typer:
            app_state.typer.speed = int(typing_speed.current.value)
        page.update()

    def change_on_top_state_chk_bx(e):
        app_state.always_on_top = e.control.value
        page.update()

    def pick_file(e):
        def file_result(result: ft.FilePickerResultEvent):
            if result.files:
                file_input.value = result.files[0].path
                page.update()
                app_state.source_file_path = result.files[0].path
                app_state.initialize_text_data(app_state.source_file_path)
                check_enable_start()
        
        file_picker.on_result = file_result
        file_picker.pick_files(allow_multiple=False)

    def check_enable_start():
        if (
            app_state.target_window and
            app_state.source_file_path and 
            app_state.target_window.parent_title
        ):
            play_button.disabled=False
            page.update()

    def start_playback(e):
        app_state.play = True
        app_state.initalize_typer()
        app_state.typer.focus_window()
        time.sleep(0.25)
        app_state.play = True
        app_state.paused = False
        if app_state.text_data and app_state.typer:
            play_button.disabled = True
            resume_button.disabled = True
            stop_button.disabled = False
            pause_button.disabled = False
            page.update()
            app_state.typer.type_text_tokens()
            print("STOPPED PLAYING")
        stop_playback(None)
        page.update()

    def pause_playback(e):
        if app_state.paused:
            resume_button.disabled = False
            pause_button.disabled = True
            advance_to_next_newline_button.disabled = False
            advance_to_next_token_button.disabled = False
            page.update()

    def resume_playback(e):
        app_state.typer.focus_window()
        time.sleep(0.25)
        app_state.paused = False
        app_state.typer.paused = False
        resume_button.disabled = True
        pause_button.disabled = False
        advance_to_next_newline_button.disabled = True
        advance_to_next_token_button.disabled = True
        page.update()
            

    def stop_playback(e):
        app_state.paused = False
        app_state.play = False
        if app_state.typer:
            app_state.typer.paused = False
            app_state.typer.play = False
        resume_button.disabled = True
        pause_button.disabled = True
        stop_button.disabled = True
        play_button.disabled = False
        advance_to_next_newline_button.disabled = True
        advance_to_next_token_button.disabled = True
        app_state.typer = None
        app_state.initialize_text_data(app_state.source_file_path)
        page.update()

    def toggle_pause_on_new_line(e):
        if pause_on_new_line_chk_bx.current.value:
            app_state.pause_on_new_line = True
            if app_state.typer:
                app_state.typer.pause_on_new_line = True
        else:
            app_state.pause_on_new_line = False
            if app_state.typer:
                app_state.typer.pause_on_new_line = False

    def start_playback_paused(e):
        if start_playback_paused_chk_bx.current.value:
            app_state.start_playback_paused = True
            if app_state.typer:
                app_state.typer.start_playback_paused = True
        else:
            app_state.start_playback_paused = False
            if app_state.typer:
                app_state.typer.start_playback_paused = False

    def on_pause_button(e):
        pause_playback(e)
    
    def on_resume_button(e):
        resume_playback(e)

    def on_advance_newline_button(e):
        if app_state.typer and app_state.play:
            app_state.typer.advance_to_newline += 1

    def on_advance_token_button(e):
        if app_state.typer and app_state.play:
            app_state.typer.advance_token += 1

    def toggle_auto_home_on_newline(e):
        if auto_home_on_newline_chk_bx.current.value:
            app_state.auto_home_on_newline = True
            if app_state.typer:
                app_state.typer.auto_home_on_newline = True
        else:
            app_state.auto_home_on_newline = False
            if app_state.typer:
                app_state.typer.auto_home_on_newline = False

    def toggle_control_on_newline(e):
        if ctrl_on_newline_chk_bx.current.value:
            app_state.control_on_newline = True
            if app_state.typer:
                app_state.typer.control_on_newline = True
        else:
            app_state.control_on_newline = False
            if app_state.typer:
                app_state.typer.control_on_newline = False

    def toggle_replace_quad_spaces_with_tab(e):
        if replace_quad_spaces_with_tab_chk_bx.current.value:
            app_state.replace_quad_spaces_with_tab = True
        else:
            app_state.replace_quad_spaces_with_tab = False




 

    ############################## VARIABLES ##############################
    keep_autotyper_window_on_top_chk_box = ft.Ref[ft.Checkbox]()
    pause_on_new_line_chk_bx = ft.Ref[ft.Checkbox]()
    start_playback_paused_chk_bx = ft.Ref[ft.Checkbox]()
    auto_home_on_newline_chk_bx = ft.Ref[ft.Checkbox]()
    ctrl_on_newline_chk_bx = ft.Ref[ft.Checkbox]()
    replace_quad_spaces_with_tab_chk_bx = ft.Ref[ft.Checkbox]()

    typing_speed = ft.Ref[ft.Slider]()
    typing_speed_label = ft.Ref[ft.Text]()

    target_application_title_text = ft.Ref[ft.TextField]()

    tokens_preview = ft.Ref[ft.TextField]()
    app_state.tokens_preview = tokens_preview
    
    file_picker = ft.FilePicker()
    file_input = ft.TextField(height=30, text_size=14, content_padding=ft.padding.Padding(5, 0, 5, 0), read_only=True)
    open_button = ft.ElevatedButton("select source file to play", on_click=pick_file, icon=ft.Icons.FILE_OPEN)

    play_button = ft.ElevatedButton("START", on_click=start_playback, icon=ft.Icons.PLAY_ARROW, disabled=True)
    pause_button = ft.ElevatedButton("PAUSE", on_click=on_pause_button, icon=ft.Icons.PAUSE, disabled=True)
    resume_button = ft.ElevatedButton("RESUME", on_click=on_resume_button, icon=ft.Icons.SKIP_NEXT, disabled=True)
    stop_button = ft.ElevatedButton("STOP", on_click=stop_playback, icon=ft.Icons.STOP, disabled=True)

    advance_to_next_newline_button = ft.ElevatedButton("ADV. NEWLINE", on_click=on_advance_newline_button, icon=ft.Icons.FAST_FORWARD, disabled=True)
    advance_to_next_token_button = ft.ElevatedButton("ADV. TOKEN", on_click=on_advance_token_button, icon=ft.Icons.FAST_FORWARD, disabled=True)


    ############################## LAYOUT ##############################
    page.add(
        ft.Text("how to use AutoTyper:", weight=ft.FontWeight.BOLD),
        ft.Text("1. select the target application\n2. select the source code file to play back\n3. adjust playback speed and settings\n4. start playback and use hotkeys to control playback"),
        ft.Divider(height=1, thickness=1, color="white"),
        ft.Divider(height=1, thickness=1, color="black"),
        ft.Divider(height=1, thickness=1, color="white"),
        ft.Text("target application window name:", weight=ft.FontWeight.BOLD),
        ft.TextField(height=30, text_size=14, content_padding=ft.padding.Padding(5, 0, 5, 0), ref=target_application_title_text, read_only=False),
        ft.ElevatedButton("select target application window", on_click=select_target_app_btn_clk, icon=ft.Icons.SELECT_ALL),
        ft.Divider(height=1, thickness=1, color="white"),
        ft.Checkbox("keep AutoTyper on top of other windows.", ref=keep_autotyper_window_on_top_chk_box, on_change=change_on_top_state_chk_bx, value=True),
        ft.Divider(height=1, thickness=1, color="white"),
        ft.Text("source file to play:", weight=ft.FontWeight.BOLD),
        file_input,
        open_button,
        file_picker,
        ft.Divider(height=1, thickness=1, color="white"),
        ft.Divider(height=1, thickness=1, color="white"),
        ft.Text("auto typing Speed: 100 ms", ref=typing_speed_label, weight=ft.FontWeight.BOLD),
        ft.Slider(min=100, max=500, divisions=16, ref=typing_speed, on_change=update_slider_label),
        ft.Row([
            ft.Checkbox("auto pause on new line", ref=pause_on_new_line_chk_bx, on_change=toggle_pause_on_new_line, value=False),
            ft.Checkbox("start playback paused", ref=start_playback_paused_chk_bx, on_change=start_playback_paused, value=False), 
        ]),
        ft.Row([
            ft.Checkbox("auto home on newline", ref=auto_home_on_newline_chk_bx, on_change=toggle_auto_home_on_newline, value=True),
            ft.Checkbox("ctrl on newline", ref=ctrl_on_newline_chk_bx, on_change=toggle_control_on_newline, value=True),
            ft.Checkbox("replace quad spaces with tab", ref=replace_quad_spaces_with_tab_chk_bx, on_change=toggle_replace_quad_spaces_with_tab, value=True),   
        ]),
        ft.Divider(height=1, thickness=4, color="white"),
        ft.Row([
            play_button,
            pause_button,
            resume_button,
            stop_button,
            advance_to_next_newline_button,
            advance_to_next_token_button
        ]),
        ft.Divider(height=1, thickness=4, color="white"),
        ft.Text("hotkeys", weight=ft.FontWeight.BOLD),
        ft.Text("source text/tokens preview area", weight=ft.FontWeight.BOLD),
        ft.Divider(height=1, thickness=1, color="black"),
        ft.Divider(height=1, thickness=1, color="white"),
        ft.Text(value="", max_lines=4, ref=tokens_preview),
    )

    # trigger all the checkbox events at start
    checkboxes = [chk_bx for chk_bx in page.controls if isinstance(chk_bx, ft.Checkbox)]
    rows = [row for row in page.controls if isinstance(row, ft.Row)]
    for row in rows:
        checkboxes.extend([chk_bx for chk_bx in row.controls if isinstance(chk_bx, ft.Checkbox)])
    for checkbox in checkboxes:
        checkbox.on_change(ft.ControlEvent(target=None, name=None, data=None, control=checkbox, page=page))


    ############################## THREADs ##############################

    def app_state_watcher(app_state):
        watched_states = {
            "paused": bool(app_state.paused),
            "play": bool(app_state.play),
            "close": bool(app_state.close)
        }
        while not app_state.close:
            if app_state.paused != watched_states["paused"]:
                if app_state.paused and app_state.play:
                    pause_playback(None)
            
            watched_states = {
                "paused": app_state.paused,
                "play": app_state.play,
                "close": app_state.close
            }
            time.sleep(0.01)
    threading.Thread(target=app_state_watcher, args=(app_state,), daemon=True).start()

    ############################ CLEANUP #####################################

    def cleanup(e):
        app_state.play = False
        app_state.paused = False
        app_state.close = True
        time.sleep(0.5)
        page.window.destroy()
    page.window.prevent_close = True
    page.window.on_event = lambda e: cleanup(e) if e.data == "close" else None

ft.app(target=main, view=ft.AppView.FLET_APP_HIDDEN)
