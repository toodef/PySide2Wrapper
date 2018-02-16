from src.app import Application
from src.window import MainWindow
from src.widget import LineEdit

app = Application()
win = MainWindow("Full sample")
le = win.add_widget(LineEdit().add_label("label", 'left'))
win.show()
app.run()
