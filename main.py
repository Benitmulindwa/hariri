from flet import *
import flet as ft


def editor_style():
    return {
        "expand": True,
        "multiline": True,
        "autofocus": True,
        "border": InputBorder.NONE,
        "height": 500,
    }


class CodeEditor(ft.TextField):
    def __init__(self, page):
        super().__init__(**editor_style())
        self.page = page

    def app_bar(self, page):
        return AppBar(
            bgcolor="#164863",
            title=Row([TextButton("File", on_click=self.run)]),
            actions=[
                IconButton(ft.icons.PLAY_ARROW, on_click=self.run),
                IconButton(ft.icons.WB_SUNNY_OUTLINED),
                PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            on_click=None,
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
                            on_click=None,
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
                            on_click=None,
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
                            on_click=None,
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
                            on_click=None,
                            content=Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Text("Exit"),
                                ],
                            ),
                        ),
                    ]
                ),
            ],
        )

    def run(self, e):
        code = self.value
        exec(code)


def main(page: ft.Page):
    page.title = "Hariri"

    myEditor = CodeEditor(page)
    page.appbar = myEditor.app_bar(page)
    page.scroll = ScrollMode.ALWAYS

    page.add(myEditor)


if __name__ == "__main__":
    ft.app(target=main)
