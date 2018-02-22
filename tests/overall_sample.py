from PySide2Wrapper.app import Application
from PySide2Wrapper.window import MainWindow
from PySide2Wrapper.widget import LineEdit, Button, ImageLayout, CheckBox


def callback():
    print("Call")


app = Application()
win = MainWindow("Full sample")
win.add_widget(LineEdit().add_label("label", 'left'))
btn = win.add_widget(Button("MyBtn").set_on_click_callback(callback))
pix = win.add_widget(ImageLayout().set_image_from_data(b"F0F0", 2, 1, 6).set_size(200, 200))
check = CheckBox("Check box sample").add_clicked_callback(callback)
check2 = CheckBox("Check box second sample").add_clicked_callback(callback)
win.add_to_group_box("Group box", [check, check2])
btn.add_enabled_dependency(check)
btn.add_enabled_dependency(check2)
win.show()
app.run()
