from flet import *
import flet as ft
import autopep8


def editor_style():
    return {
        "expand": True,
        "multiline": True,
        "autofocus": True,
        "border": InputBorder.NONE,
        "height": 500,
    }


class CodeEditor(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.on_keyboard_event = self.on_keyboard

    def build(self):
        # App bar
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
                    on_click=self.save_as_clicked,
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

        self.page.overlay.append(
            Container(
                padding=5,
                expand=True,
                bgcolor="#164863",
                content=Row([self.file_menu]),
            )
        )
        self.main_ft = TextField(**editor_style())
        return Column(controls=[Divider(opacity=0), self.main_ft])

    def new_clicked(self, e):
        self.value = ""
        self.update()

    # Open a file
    def open_clicked(self, e):
        file_picker = FilePicker(on_result=self.open_file_result)
        self.page.overlay.append(file_picker)
        self.page.update()

        file_picker.pick_files(
            allow_multiple=False, allowed_extensions="py", dialog_title="Open File"
        )

    def open_file_result(self, e: FilePickerResultEvent):
        print(e.files)

    def save_clicked(self, e):
        print("save clicked")

    def save_as_clicked(self, e):
        print("Save_as clicked")

    def exit(self, e):
        print("exit clicked")

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
        code = self.value
        exec(code)


def main(page: ft.Page):
    page.title = "Hariri"

    myEditor = CodeEditor(page)
    page.scroll = ScrollMode.ALWAYS

    page.add(myEditor)


if __name__ == "__main__":
    ft.app(target=main)


###-----------------------------------------------------------------------------------------------------------------------------------#####
