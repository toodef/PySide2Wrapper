from PySide2Wrapper.app import Application
from PySide2Wrapper.window import MainWindow
from PySide2Wrapper.widget import LineEdit, Button, ImageLayout


def callback():
    print("Call")


app = Application()
win = MainWindow("Full sample")
win.add_widget(LineEdit().add_label("label", 'left'))
win.add_widget(Button("MyBtn").set_on_click_callback(callback))
pix = win.add_widget(ImageLayout().set_image_from_data(b"F0F0", 2, 1, 6).set_size(200, 200))
win.show()
app.run()
