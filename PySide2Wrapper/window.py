from abc import ABCMeta, abstractmethod

from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QDialog, QWidget, QLabel
from .widget import Widget


class AbstractWindow(metaclass=ABCMeta):
    def __init__(self, title: str, widget: QWidget):
        self._widget = widget
        self._widget.setWindowTitle(title)
        self.__layouts = [QVBoxLayout()]
        self._widget.setLayout(self.get_current_layout())

    @abstractmethod
    def show(self):
        """
        Show this window
        :return:
        """

    def add_widget(self, widget: Widget):
        """
        Add widget to window layout
        :param widget: Widget unit
        :return: widget instance
        """
        self.get_current_layout().addLayout(widget.get_layout())
        return widget

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
        layout = QHBoxLayout()
        self.get_current_layout().addLayout(layout)
        self.__layouts.append(layout)

    def start_vertical(self):
        """
        Start vertical components insertion
        :return: None
        """
        if isinstance(self.get_current_layout(), QVBoxLayout):
            return
        layout = QVBoxLayout()
        self.get_current_layout().addLayout(layout)
        self.__layouts.append(layout)

    def group_horizontal(self, widgets: list):
        """
        Place list of widgets horizontal
        :param widgets: list of widgets
        :return: None
        """
        self.start_horizontal()
        self.add_widgets(widgets)
        self.cancel()

    def group_vertical(self, widgets: [Widget]):
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

    def add_to_group_box(self, group_name: str, widgets: [Widget]):
        """
        Place layout to group box
        :param group_name: name of group
        :param widgets: list of widgets, that been placed to group
        :return: None
        """
        self.start_group_box(group_name)
        for widget in widgets:
            self.add_widget(widget)
        self.cancel()

    def start_group_box(self, name: str):
        """
        Start group box
        :return:
        """
        group_box = QGroupBox(name)
        group_box_layout = QVBoxLayout()
        group_box.setLayout(group_box_layout)
        self.get_current_layout().addWidget(group_box)
        self.__layouts.append(group_box_layout)

    def cancel(self):
        """
        Cnacel last format append
        :return: None
        """
        del self.__layouts[-1]

    def get_instance(self):
        return self._widget

    def insert_text_label(self, text, is_link=False):
        widget = QLabel(text)
        widget.setOpenExternalLinks(is_link)
        self.get_current_layout().addWidget(widget)


class Window(AbstractWindow):
    def __init__(self, title: str=""):
        super().__init__(title, QDialog())

    def show(self):
        self._widget.exec_()


class MainWindow(AbstractWindow):
    def __init__(self, title: str=""):
        super().__init__(title, QWidget())

    @staticmethod
    def add_subwindow(title: str):
        """
        Create subwindow
        :param title: window title
        :return: window
        @rtype Window
        """
        return Window(title)

    def show(self):
        self._widget.show()
