from flet import *
import flet as ft
import autopep8


def editor_style():
    return {
        # "expand": True,
        "multiline": True,
        "autofocus": True,
        "border": InputBorder.NONE,
        "height": 500,
    }


class CodeEditor(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.title_suffix = " -Hariri"
        self.page.title = "New File" + self.title_suffix

        self.page.on_keyboard_event = self.on_keyboard

    def build(self):
        ## APPBAR ##

        # File popupmenu
        self.file_menu = ft.PopupMenuButton(
            content=Text("File", size=15),
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

        # Icons Buttons

        self.page.overlay.append(
            Container(
                padding=5,
                expand=True,
                bgcolor="#164863",
                content=Row([self.file_menu]),
            )
        )
        self.main_ft = TextField(**editor_style())
        return Column([Divider(opacity=0), self.main_ft])

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
        file_path = e.files[0].path
        self.file_name = e.files[0].name
        self.page.title = self.file_name + self.title_suffix

        with open(file_path, "r") as file:
            self.main_ft.value = file.read()
            self.main_ft.update()
            self._snackbar(f"File {file_path} Opened", Icon(icons.CHECK, color="black"))
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
        code = self.value
        formatted_code = autopep8.fix_code(code)
        self.code = ""
        self.value = formatted_code

    # Adding shortcuts

    def on_keyboard(self, e: ft.KeyboardEvent):
        if e.ctrl and e.key == "N":
            self.new_clicked(e)
        elif e.ctrl and e.key == "O":
            self.open_clicked(e)
        elif e.ctrl and e.key == "S":
            self.save_clicked(e)
        elif e.ctrl and e.shift and e.key == "S":
            self.save_as_clicked(e)
        elif e.key == "Tab":
            print(self.value.splitlines()[-1])

    def run(self, e):
        code = self.main_ft.value
        exec(code)


def main(page: ft.Page):
    page.title = "Hariri"

    myEditor = CodeEditor(page)
    page.scroll = ScrollMode.ALWAYS

    page.add(myEditor)


if __name__ == "__main__":
    ft.app(target=main)


###-----------------------------------------------------------------------------------------------------------------------------------#####
