import flet as ft


class Task(ft.Container):
    def __init__(self, txt):
        super().__init__()

        self.txt = txt
        self.input_field = ft.TextField(self.txt, expand=True)
        self.check_box = ft.Checkbox(self.txt, expand=True)
        self.display_view = ft.Row(
            controls=[
                self.check_box,
                ft.IconButton(icon=ft.icons.CREATE_OUTLINED, on_click=self.edit_task),
                ft.IconButton(icon=ft.icons.DELETE_OUTLINE, on_click=self.delete_item)
            ]
        )

        self.edit_view = ft.Row(
            controls=[
                self.input_field,
                ft.IconButton(icon=ft.icons.DONE, on_click=self.save)
            ]
        )
        self.content = self.display_view

    def delete_item(self, e):
        self.parent.controls.remove(self)
        self.page.update()

    def edit_task(self, e):
        print("edit task.....")
        self.content = self.edit_view
        self.page.update()

    def save(self, e):
        self.txt = self.input_field.value
        self.check_box.label = self.txt
        self.content = self.display_view
        self.page.update()


class Todo(ft.Column):
    def __init__(self):
        super().__init__(width=600)

        self.input_field = ft.TextField("", hint_text="entddder task name", expand=True)
        self.navigation = ft.Row()
        self.task_list = ft.Column()
        # self.width = 600,
        self.filters = ft.Tabs(
            mouse_cursor=ft.MouseCursor.CLICK,
            selected_index=0,
            on_change=self.filter_tasks,
            tabs=[
                ft.Tab(text="all"),
                ft.Tab(text="active"),
                ft.Tab(text="complete"),
            ]
        )
        self.controls = [
            ft.Row(
                controls=[
                    self.input_field,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD,
                        # mouse_cursor=ft.MouseCursor.CLICK,
                        on_click=self.add_task,
                    ),
                    # input_field
                ],
            ),
            self.filters,
            self.task_list
        ]

    def add_task(self, e: ft.TapEvent):
        if self.input_field.value:
            self.task_list.controls.append(Task(self.input_field.value))
        self.input_field.value = ""
        e.control.bgcolor = ft.colors.random_color()
        print("sdf")
        # e.target.bgcolor=ft.colors.random_color()
        self.update()
        # print(ft.colors)

    def filter_tasks(self, e):
        print(e.control.selected_index)
        # self.before_update()
        # self.task_list.update()
        # self.task_list.update()
        # self.tas()

    def before_update(self):
        super().before_update()
        print("before update")
        status = self.filters.selected_index
        for task in self.task_list.controls:
            task.visible = (
                    status == 0
                    or (status == 1 and not task.check_box.value)
                    or status == 2 and task.check_box.value
            )
            print(status, task.visible, task.check_box.value)


class TestTodo(ft.Column):
    def __init__(self):
        self.width = 300
        super().__init__(width=300)
        self.controls.append(
            ft.Row(
                controls=[
                    ft.TextField(hint_text="enter"),
                    # ft.FloatingActionButton(icon=ft.icons.ADD)
                ]
            )
        )

# Todo = TestTodo
