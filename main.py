from flet import *
import flet as ft
import autopep8
import subprocess


def editor_style():
    return {
        "expand": True,
        "multiline": True,
        "autofocus": True,
        "border": InputBorder.NONE,
        "height": 450,
    }


class CodeEditor(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        # self.page.theme_mode = ft.ThemeMode.LIGHT
        self.title_suffix = " -Hariri"
        self.current_file_path = ""
        self.page.title = "New File" + self.title_suffix
        self.page.on_keyboard_event = self.on_keyboard
        self.clicked = 0

    def build(self):
        ## APPBAR ##
        self._file_txt = Container(content=Text("File", size=20))
        self._file_txt.padding = padding.only(left=10)
        # File popupmenu
        self.file_menu = ft.PopupMenuButton(
            content=self._file_txt,
            items=[
                ft.PopupMenuItem(
                    on_click=self.new_clicked,
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text("New File"),
                            VerticalDivider(),
                            Text("CTRL + N"),
                        ],
                    ),
                ),
                ft.PopupMenuItem(
                    on_click=self.open_clicked,
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text("Open"),
                            VerticalDivider(),
                            Text("CTRL + O"),
                        ],
                    ),
                ),
                ft.PopupMenuItem(
                    on_click=self.save_clicked,
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text("Save"),
                            VerticalDivider(),
                            Text("CTRL + S"),
                        ],
                    ),
                ),
                ft.PopupMenuItem(
                    on_click=self.save_as,
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text("Save As"),
                            VerticalDivider(),
                            Text("CTRL + Shift + S"),
                        ],
                    ),
                ),
                ft.PopupMenuItem(),
                ft.PopupMenuItem(
                    on_click=self.exit,
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text("Exit"),
                        ],
                    ),
                ),
            ],
        )

        ## TERMINAL ##

        self.terminal = TextField(
            multiline=True,
            autofocus=True,
            border=InputBorder.NONE,
            value=self.current_file_path,
            text_size=15,
        )

        self._terminal = ListView(
            height=180,
            spacing=15,
            auto_scroll=True,
        )
        self._terminal.controls.append(self.terminal)

        # Icons Buttons

        self.dark_light_icon = IconButton(
            icon=icons.DARK_MODE_ROUNDED, on_click=self.switch, data=True
        )

        self.run_icon = IconButton(
            icon=icons.PLAY_ARROW,
            on_click=self.run,
        )

        ## Overlay_content ##

        self.overlay_content = Container(
            padding=5,
            expand=True,
            bgcolor="#164863",
            content=Row(
                controls=[
                    self.file_menu,
                    Row(expand=True),
                    self.run_icon,
                    self.dark_light_icon,
                ]
            ),
        )

        self.page.overlay.append(self.overlay_content)
        self.main_ft = TextField(
            **editor_style(),
            text_style=TextStyle(font_family="SourceCode")
            # on_submit=self.format_code,
        )

        return Column(
            controls=[
                Column(
                    controls=[
                        Divider(height=8, opacity=0),
                        Row(
                            controls=[self.main_ft],
                        ),
                    ],
                ),
                Divider(height=8, opacity=3),
                self._terminal,
            ],
        )

    ## Dark-light-mode ##

    def switch(self, e):
        if e.control.data == True:
            self.clicked += 1
            if self.clicked % 2 != 0:
                self.page.theme_mode = ThemeMode.LIGHT
                self._file_txt.color = "#164863"

                self.run_icon.icon_color = "#164863"
                self.dark_light_icon.icon_color = "#164863"
                self.dark_light_icon.icon = icons.DARK_MODE_ROUNDED
                self.overlay_content.bgcolor = "#9bbec8"

                self.main_ft.text_style.font_family = "SourceCodeBlack"
                # self.main_ft.text_style.color = "#164863"
                self.main_ft.update()

            else:
                self.dark_light_icon.icon = icons.LIGHT_MODE_ROUNDED
                self.overlay_content.bgcolor = "#164863"
                self.dark_light_icon.icon_color = "white"
                self.run_icon.icon_color = "white"
                self.page.theme_mode = ThemeMode.DARK
            self.page.update()

    def new_clicked(self, e):
        self.main_ft.value = ""
        self.main_ft.update()

    # Open a file
    def open_clicked(self, e):
        file_picker = FilePicker(on_result=self.open_file_result)
        self.page.overlay.append(file_picker)
        self.page.update()

        file_picker.pick_files(
            allow_multiple=False, allowed_extensions=["py"], dialog_title="Open File"
        )

    def open_file_result(self, e: FilePickerResultEvent):
        self.file_path = e.files[0].path
        self.file_name = e.files[0].name
        self.page.title = self.file_name + self.title_suffix

        with open(self.file_path, "r") as file:
            self.main_ft.value = file.read()
            self.main_ft.update()
            self._snackbar(
                f"File {self.file_path} Opened", Icon(icons.CHECK, color="black")
            )

        self.current_file_path = self.file_path
        self.page.update()
        self.terminal.value = self.current_file_path + ">"
        self.terminal.update()

    def save_as(self, e):
        file_picker = FilePicker(on_result=self.save_as_result)
        self.page.overlay.append(file_picker)
        self.page.update()

        file_picker.save_file(
            file_name="New File", allowed_extensions=["py"], dialog_title="Save As"
        )

    def save_as_result(self, e: ft.FilePickerResultEvent):
        with open(e.path, "w") as file:
            file.write(self.main_ft.value)
            self.current_file_path = e.path

        file_name = e.path.split("\\")
        self.page.title = file_name[-1] + self.title_suffix
        self._snackbar(f"Saved As {file_name[-1]}", Icon(icons.CHECK, color="green"))
        self.page.update()

    def save_clicked(self, e):
        if self.current_file_path == "":
            self.save_as(e)
        with open(self.current_file_path, "r") as file:
            self.is_different = self.main_ft.value != file.read()
            if self.is_different:
                with open(self.current_file_path, "w") as new_script:
                    new_script.write(self.main_ft.value)
                    self.is_code_different = False
                    self._snackbar("Saved", Icon(icons.THUMB_UP_OFF_ALT))
                    self.page.update()
            else:
                pass

    def exit(self, e):
        print("exit clicked")

    # snackbar

    def _snackbar(self, text: str, icon: Icon):
        self.page.snack_bar = SnackBar(
            bgcolor="#427d9d",
            open=True,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[Text(text, color="black"), icon],
            ),
        )

    # formatting the code

    def format_code(self, e):
        print("Submitted!!")
        code = self.main_ft.value

        # Format the code
        formatted_code = autopep8.fix_code(code)
        self.main_ft.value = ""
        self.main_ft.value = formatted_code
        self.main_ft.update()

    # Adding keyboard shortcuts

    def on_keyboard(self, e: ft.KeyboardEvent):
        if e.ctrl and e.key == "N":
            self.new_clicked(e)
        elif e.ctrl and e.key == "O":
            self.open_clicked(e)
        elif e.ctrl and e.key == "S":
            self.save_clicked(e)
        elif e.ctrl and e.shift and e.key == "S":
            self.save_as_clicked(e)
        elif e.shift and e.key == "R":
            self.run(e)

    def run(self, e):
        # check if the file is saved before running it

        self.save_clicked(e)
        process = subprocess.Popen(
            ["python", self.current_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True,
        )
        output, error = process.communicate()
        if output:
            self.terminal.color = "white"
            self.terminal.value = self.current_file_path + "\n" + output
            self.terminal.update()
        else:
            self.terminal.color = "red"
            self.terminal.value = error
            self.terminal.update()


def main(page: ft.Page):
    page.title = "Hariri"
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {
        "SourceCode": "fonts/SourceCodePro-Light.ttf",
        "SourceCodeBold": "fonts/SourceCodePro-Bold.ttf",
        "SourceCodeBlack": "fonts/SourceCodePro-Black.ttf",
    }

    myEditor = CodeEditor(page)

    page.add(Divider(height=10), myEditor)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")


###-----------------------------------------------------------------------------------------------------------------------------------#####
