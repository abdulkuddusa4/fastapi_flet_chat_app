# import time
# from contextlib import asynccontextmanager
#
# import flet
# from fastapi import FastAPI, Request, WebSocket
# from fastapi.responses import RedirectResponse
#
# from api.common.db.sql import engine
# from api.auth import router as auth_router
# from api.config import BASE_DIR
# from sqlmodel import SQLModel
# import flet_fastapi
# from ui.main import main as main_ui
#
# # flet_app =
# app = FastAPI()
#
#
# @app.on_event("startup")
# async def startup():
#     SQLModel.metadata.create_all(engine)
#     pass
#
#
# #
# # @app.on_event("shutdown")
# # async def startup():
# #     print("shutdown")
# #     await flet_fastapi.app_manager.shutdown()
# #     pass
#
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await flet_fastapi.app_manager.start()
#     yield
#     await flet_fastapi.app_manager.shutdown()
#
#
# class UiCom(flet.Container):
#     def __init__(self):
#         super().__init__()
#         self.width = 100
#         self.height = 100
#         self.bgcolor = flet.colors.BLUE
#
#     # def before_update_async(self):
#     #     super().before_update_async()
#     #     print("called")
#
#     # def _get_control_name(self):
#     #     return "my con"
#
#
# def f():
#     print('function called')
#
#
# async def my_ui(page: flet.Page):
#     await page.add_async(UiCom())
#     print(UiCom().__dir__())
#     await page.controls[0].update_async()
#
#
# flet_fastapi_app = flet_fastapi.app(main_ui)
# app.mount('/ui', flet_fastapi_app)
#
# app.include_router(
#     router=auth_router,
#     prefix='/auth'
# )
#
#
# @app.websocket("/ws")
# async def f(ws: WebSocket):
#     print("websofsdfsdf")
#     await ws.accept()
#
#
# @app.get('/')
# async def home():
#     return RedirectResponse('/ui')
import flet

# from ui.main import main
def m(page):
    page.appbar = flet.AppBar()
flet.app(target=m)