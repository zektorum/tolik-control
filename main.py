from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.slider import MDSlider

from kivy.core.window import Window

from serial import Serial

from tools import move_servo


class ImprovedSlider(MDSlider):
    def __init__(self, **kwargs):
        self.slider_id = kwargs["slider_id"]
        kwargs.pop("slider_id")
        super().__init__(**kwargs)
        self.current_value = int(float(self.value))
        self.serial_device = Serial("/dev/ttyUSB0", 10100)

    def on_touch_up(self, touch):
        if super().on_touch_up(touch):
            self.active = False
        if move_servo(self.serial_device, self.slider_id + 1, self.current_value, int(self.value)) is not None:
            self.current_value = int(self.value)


class Container(MDGridLayout):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.cols = 1
        self.padding = 50
        self.spacing = 50
        self.current_slider = 0
        self.sliders = [
            ImprovedSlider(
                min=0,
                max=180,
                value=100,
                step=20,
                slider_id=i
            ) for i in range(6)
        ]
        for i in range(6):
            self.add_widget(self.sliders[i])


class MyApp(MDApp):
    def build(self):
        self.title = "Tolik Control Panel"
        return Container()


if __name__ == "__main__":
    Window.size = (800, 600)
    MyApp().run()
