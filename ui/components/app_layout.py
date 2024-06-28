import asyncio

import flet
from flet import (
    Control,
    Column,
    Container,
    IconButton,
    Page,
    Row,
    Text,
    IconButton,
    colors,
    icons,
)

from .login import Login
from .sidebar import Sidebar


class AppLayout(Row):
    def __init__(
            self,
            app,
            page: Page,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.app = app
        self.expand = True
        self.vertical_alignment = 'start'
        self.spacing = 0
        # self.alignment = flet.MainAxisAlignment.START
        self.page = page
        self.sidebar = Sidebar(self, page)
        self.sidebar.visible = False

        self.toggle_nav_rail_button = IconButton(
            icon=icons.ARROW_CIRCLE_RIGHT,
            icon_color=colors.BLUE,
            selected=True if self.sidebar.visible else False,
            selected_icon=icons.ARROW_CIRCLE_LEFT,
            on_click=self.toggle_nav_rail,
            selected_icon_color=colors.BLUE,
            icon_size=30,
            # bgcolor=colors.BLACK
        )

        count = 0
        self.active_view: Control = flet.Container(
            alignment=flet.alignment.center,
            expand=True,
            content=Text("sdf"),
            width=float('inf'),
            # bgcolor=colors.GREY,
            height=float('inf')
        )
        self.controls = [
            self.sidebar,
            self.toggle_nav_rail_button,
            self.active_view
        ]

    # def toggle_nav_rail(self, e):
    #     self.sidebar.visible = not self.sidebar.visible
    #     self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
    #
    #     self.page.update()

    async def toggle_nav_rail(self, e):
        self.sidebar.offset = flet.transform.Offset(0, 0)
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        # self.page.session.
        if not await self.page.client_storage.contains_key_async('token'):
            await self.page.client_storage.set_async('token', "sdfsdf")
            print("session set")
            print(await self.page.client_storage.get_keys_async('token'))
        print("printing session", await self.page.client_storage.get_async('token'))
        # print("side offset", self.sidebar.offset)

        await self.page.update_async()
