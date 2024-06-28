import flet
from flet import (
    colors,
    Icon,
    Text,
    Container,
    AppBar,
    icons
)

from . import trello
from . login import Login


class TrelloAppbar(AppBar):
    def __init__(self, app):
        super().__init__()
        self.app = app
        # self.appbar_items = None
        self.bgcolor = colors.BLUE
        self.leading = Icon(icons.GRID_GOLDENRATIO_ROUNDED)
        self.leading_width = 100,
        # self.title = Text("Trolli", size=32, text_align="start")
        self.title = flet.TextButton(
            content=Text("Trolli", size=32, text_align="start"),
            # on_click=
        )
        self.center_title = False,
        self.toolbar_height = 75,
        self.appbar_default_items = [
            flet.PopupMenuItem(
                text="Log Ins",
                icon=icons.LOGIN_ROUNDED,
                on_click=self.show_login_page
            ),
            flet.PopupMenuItem(),  # divider
        ]

        self.pop_up_menu = flet.PopupMenuButton(
            icon=icons.PERSON_ROUNDED,
            items=self.appbar_default_items,
        )

        self.actions = [
            Container(
                shape=flet.BoxShape.CIRCLE,
                content=self.pop_up_menu,
                margin=flet.margin.only(left=50, right=25),
                bgcolor=colors.BLUE_300
            ),
        ]

    def __await__(self):
        return self.ainit().__await__()

    async def ainit(self):
        if user_info := await self.app.page.client_storage.get_async('user_info'):
            appbar_items = [
                flet.PopupMenuItem(
                    text=user_info.get('full_name'),
                    icon=icons.PERSON_ROUNDED
                ),
                flet.PopupMenuItem(),
                flet.PopupMenuItem(
                    icon=icons.LOGOUT_ROUNDED,
                    text="Log Out",
                    on_click=self.logout
                )
            ]
            self.pop_up_menu.items = appbar_items
        else:
            self.pop_up_menu.items = self.appbar_default_items
        print(f"color: {self.bgcolor}")
        return self

    async def logout(self, e):
        await self.page.client_storage.remove_async('token')
        print(await self.page.client_storage.get_async('token'))
        print('restarting app', await self.page.client_storage.get_async('token'))
        await trello.TrelloApp(self.page)

    async def show_login_page(self, e):
        self.app.app_layout.active_view.content = Login(self.page)
        await self.app.app_layout.update_async()
