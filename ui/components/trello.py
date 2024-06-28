import json
import random

from fastapi import status
import flet
import flet_core.icons
import httpx
from flet import (
    Container,
    Icon,
    Page,
    Text,
    AppBar,
    PopupMenuButton,
    PopupMenuItem,
    colors,
    icons,
    margin
)

from .app_layout import AppLayout
from .appbar import TrelloAppbar
from .login import Login


class TrelloApp(flet.View):
    def __init__(self, page: Page):
        super().__init__()
        self.appbar = None
        print("trello app initializing")
        self.page = page

        self.app_layout = AppLayout(self, page)
        print("tr.>;g;;;;;")

        # self.page.update_async()

    async def show_login_page(self, e):
        self.app_layout.active_view.content = Login(self.page)
        self.page.views.append(Login(self.page))
        await self.page.update_async()

    async def set_navigation(self, e):
        print("called...")

    def __await__(self):
        # return self.ainit()
        # token = yield from self.page.client_storage.get_async('token').__await__()
        # self.pop_up_menu.items = self.appbar_items
        return self.ainit().__await__()

    async def ainit(self):
        await self.page.clean_async()
        self.appbar = await TrelloAppbar(self)
        # self.page.appbar = self.appbar
        # self.page.controls = [self.app_layout]
        self.controls = [self.app_layout]

        token = await self.page.client_storage.get_async('token')
        print(f"token>>:>{token}")
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "http://127.0.0.1:8000/auth/profile",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )
            if res.status_code == status.HTTP_200_OK:
                await self.page.client_storage.set_async('user_info', res.json())

        # await self.update_async()
        return self

    async def click_event(self, e):
        print("clicked")
        await self.page.clean_async()
