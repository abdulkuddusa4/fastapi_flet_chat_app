import flet as ft


class BaseButton(ft.ElevatedButton):
    def __init__(self, text, onclick, expand=1):
        super().__init__()
        self.on_click = onclick
        self.text = text
        self.data = text
        self.expand = expand


class ActionButton(BaseButton):
    def __init__(self, text, onclick, expand=1):
        super().__init__(text, onclick, expand=1)
        self.bgcolor = ft.colors.WHITE
        self.color = ft.colors.BLACK
        # self.


class DigitButton(BaseButton):
    def __init__(self, text, onclick, expand=1):
        super().__init__(text, onclick, expand)
        self.bgcolor = ft.colors.BLACK
        self.color = ft.colors.WHITE


class ExtraActionButton(BaseButton):
    def __init__(self, text, onclick, expand=1):
        super().__init__(text, onclick, expand)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class Calculator(ft.Container):
    def __init__(self):
        super().__init__(
            width=400,
        )
        # self.width = 200
        # self.height = 200
        self.border_radius = 20
        self.bgcolor = ft.colors.BLACK
        self.padding = 50
        self.exp = ["0"]
        self.head_display = ft.Text("0", color=ft.colors.WHITE)
        self.is_number = True
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.head_display], alignment=ft.MainAxisAlignment.END),
                ft.Row(
                    controls=[
                        ActionButton("AC", onclick=self.button_clicked),
                        # ActionButton("+/-", onclick=self.button_clicked),
                        ActionButton("%", onclick=self.button_clicked),
                        ExtraActionButton("/", onclick=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("7", onclick=self.button_clicked),
                        DigitButton("8", onclick=self.button_clicked),
                        DigitButton("9", onclick=self.button_clicked),

                        ExtraActionButton("*", onclick=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("4", onclick=self.button_clicked),
                        DigitButton("5", onclick=self.button_clicked),
                        DigitButton("6", onclick=self.button_clicked),

                        ExtraActionButton("+", onclick=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("1", onclick=self.button_clicked),
                        DigitButton("2", onclick=self.button_clicked),
                        DigitButton("3", onclick=self.button_clicked),
                        ExtraActionButton("-", onclick=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("0", onclick=self.button_clicked, expand=2),
                        DigitButton(".", onclick=self.button_clicked),
                        ExtraActionButton("=", onclick=self.button_clicked),
                    ]
                )

            ]
        )

    def button_clicked(self, e: ft.TapEvent):
        if isinstance(e.control, DigitButton):
            if self.is_number:
                if self.exp[-1] == '0':
                    self.exp[-1] = e.control.data
                    print("...")
                else:
                    self.exp[-1] = self.head_display.value + e.control.data
                self.head_display.value = self.exp[-1]
                self.head_display.update()
                print(self.exp)
                return

            self.is_number = True
            self.head_display.value = e.control.data
            self.exp.append(e.control.data)
            self.update()
            return
        print(self.exp)
        if isinstance(e.control, ActionButton | ExtraActionButton):
            if e.control.data == 'AC':
                self.head_display.value = "0"
                self.exp = ["0"]
                self.head_display.update()
                return
            if e.control.data == '=':
                self.exp = [str(eval(''.join(self.exp)))]
                self.head_display.value = self.exp[-1]
                self.head_display.update()
                return
                pass
            if self.is_number:
                self.is_number = False
                self.exp = [str(eval(''.join(self.exp)))]
                self.head_display.value = self.exp[-1]
                self.head_display.update()
                if e.control.data == '=':
                    return
                self.exp.append(e.control.data)
                return
                pass
            self.exp[-1] = e.control.data

            self.op = e.control.data
        self.head_display.update()
        pass
