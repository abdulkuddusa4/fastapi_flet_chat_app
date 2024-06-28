import flet as ft
from flet import (
    Page,
    colors
)

from components.trello import TrelloApp

print("..>>")
async def main(page: Page):
    print("ddd")
    page.title = "Flet Trello clone"
    page.padding = 0
    page.bgcolor = colors.BLUE_GREY_200
    page.views.append(await TrelloApp(page))

    await page.update_async()



