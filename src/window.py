from PySide2.QtWidgets import QLayout, QVBoxLayout, QHBoxLayout, QWidget
from .widget import Widget


class Window:
    def __init__(self, title: str = ""):
        self.__widget = QWidget()
        self.__widget.setWindowTitle(title)
        self.__layouts = [QVBoxLayout()]

    def show(self):
        """
        Show this window
        :return:
        """
        self.__widget.show()

    def add_widget(self, widget: Widget):
        """
        Add widget to window layout
        :param widget: Widget unit
        :return: None
        """
        self.get_current_layout().addWidget(widget)

    def add_widgets(self, widgets: [Widget]):
        """
        Add list of widgets to window layout
        :param widgets: Widget units
        :return: None
        """
        for widget in widgets:
            self.get_current_layout().addLayout(widget.get_layout())

    def start_horizontal(self):
        """
        Start horizontal components insertion
        :return: None
        """
        if isinstance(self.get_current_layout(), QHBoxLayout):
            return

        self.__layouts.append(QHBoxLayout())

    def start_vertical(self):
        """
        Start vertical components insertion
        :return: None
        """
        if isinstance(self.get_current_layout(), QVBoxLayout):
            return

        self.__layouts.append(QVBoxLayout())

    def group_horizontal(self, widgets: list):
        """
        Place list of widgets horizontal
        :param widgets: list of widgets
        :return: None
        """
        self.start_horizontal()
        self.add_widgets(widgets)
        self.cancel()

    def group_vertical(self, widgets):
        """
        Place list of widgets vertical
        :param widgets: list of widgets
        :return: None
        """
        self.start_vertical()
        self.add_widgets(widgets)
        self.cancel()

    def get_current_layout(self):
        """
        Return current layout
        :return: layout of type QLayout
        """
        return self.__layouts[-1]

    def add_to_group_box(self, group_name: str, layout: QLayout):
        """
        Place layout to group box
        :param group_name: name of group
        :param layout: layout, that been placed to group
        :return: None
        """
        pass

    def start_group_box(self, name: str):
        """
        Start group box
        :return:
        """
        pass

    def cancel(self):
        """
        Cnacel last format append
        :return: None
        """
        del self.__layouts[-1]


class MainWindow(Window):
    def __init__(self, title: str=""):
        super().__init__(title)

    @staticmethod
    def add_subwindow(title: str):
        """
        Create subwindow
        :param title: window title
        :return: window
        @rtype Window
        """
        return Window(title)
