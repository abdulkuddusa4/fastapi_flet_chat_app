import flet

from ui.components.app_layout import AppLayout


class Chat:
    def __init__(self, page: flet.Page):
        self.page = page
        self.app_layout = AppLayout()

    def __await__(self):
        return self.ainnit().__await__()

    async def ainnit(self):
        await self.page.clean_async()
        pass
