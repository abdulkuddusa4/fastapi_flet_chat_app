import asyncio

import flet
import flet as ft
import httpx
from starlette import status

from . import trello


class Login(ft.Container):
    def __init__(self, page):
        super().__init__()

        self.page = page
        self.page.title = "login"
        self.height = float('inf')
        self.width = 550
        # self.height = float('inf')
        # self.alignment = flet.Alignment(
        #     x=20,
        #     y=20
        # )
        self.padding = ft.Padding(20, 110, 20, 70)
        self.email_field = ft.TextField(
            hint_text="xyz@domain.com",
            border_width=0,
            bgcolor=ft.colors.WHITE,
            hint_style=ft.TextStyle(color=ft.colors.BLUE_300),
            width=float('inf'),
            color=ft.colors.BLUE
        )
        self.password_field = ft.TextField(
            password=True,
            hint_text="********",
            border_width=0,
            bgcolor=ft.colors.WHITE,
            hint_style=ft.TextStyle(color=ft.colors.BLUE_300),
            width=float('inf'),
            color=ft.colors.BLUE,
            on_submit=self.login
        )
        self.name = 'login'
        # self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.bgcolor = ft.colors.BLUE
        # self.expand = True
        # self.controls = [
        #     self.email_field
        # ]

        # print(self.page.client_storage.get_async)
        self.content = ft.Column(
            # expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.email_field,
                self.password_field,
                flet.ElevatedButton(
                    text="Log in",
                    on_click=self.login

                )
            ]
        )
        self.height = float('inf')
        # self.bgcolor =

    async def login(self, e):

        async with httpx.AsyncClient() as client:
            res = await client.post(
                "http://127.0.0.1:8000/auth/login",
                json={
                    'email': self.email_field.value,
                    "password": self.password_field.value
                }
            )
            if res.status_code == status.HTTP_200_OK:
                await self.page.client_storage.set_async('token', res.json().get('token'))
                await self.page.update_async()
                print()
                await trello.TrelloApp(self.page)
        pass

    def build(self):
        return flet.Text("dddddddddddd")
