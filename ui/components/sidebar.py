import flet
from flet import (
    UserControl,
    Column,
    Container,
    Row,
    Text,
    NavigationRail,
    NavigationRailDestination,
    alignment,
    border_radius,
    colors,
    icons,
    padding,
    margin,
)


class Sidebar(flet.Column):

    def __init__(self, app_layout, page):
        super().__init__(height=float('inf'), width=200)
        self.app_layout = app_layout
        # self.expand = True
        # self.offset = flet.Offset(-self.width, 0)
        self.bgcolor = flet.colors.RED
        self.page = page
        # self.animate_offset = flet.transform.Offset(1,0)
        self.top_nav_items = [
            NavigationRailDestination(
                label_content=Text("Boards"),
                label="Boards",
                icon=icons.BOOK_OUTLINED,
                selected_icon=icons.BOOK_OUTLINED
            ),
            NavigationRailDestination(
                label_content=Text("Members"),
                label="Members",
                icon=icons.PERSON,
                selected_icon=icons.PERSON
            ),

        ]
        self.top_nav_rail = NavigationRail(
            selected_index=0,
            label_type="all",
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.BLUE_GREY,
            # width=200,
            # height=float('inf')
            # extended=True,
            expand=True
        )

        self.controls = [
            self.top_nav_rail
        ]

    # def build(self):
    #     print("build called")
    #     self.view = Container(
    #
    #         content=Column([
    #             Row([
    #                 Text("Workspace"),
    #             ]),
    #             # divider
    #             Container(
    #                 bgcolor=colors.BLACK26,
    #                 border_radius=border_radius.all(30),
    #                 height=1,
    #                 alignment=alignment.center_right,
    #                 width=220
    #             ),
    #             self.top_nav_rail,
    #             # divider
    #             Container(
    #                 bgcolor=colors.BLACK26,
    #                 border_radius=border_radius.all(30),
    #                 height=100,
    #                 alignment=alignment.center_right,
    #                 width=220
    #             ),
    #         ], tight=True),
    #         padding=padding.all(15),
    #         margin=margin.all(0),
    #         width=250,
    #         bgcolor=colors.RED,
    #     )
    #     return self.view

    async def top_nav_change(self, e):
        self.top_nav_rail.selected_index = e.control.selected_index
        await self.update_async()

    # def _get_control_name(self):
    #     return "no name"
