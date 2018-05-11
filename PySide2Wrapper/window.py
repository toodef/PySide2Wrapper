from abc import ABCMeta, abstractmethod

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QDialog, QWidget, QLabel, QDockWidget, \
    QScrollArea
from .widget import Widget, Button, ProgressBar


class AbstractWindow(metaclass=ABCMeta):
    def __init__(self, title: str, widget: QWidget, enable_scrolling: bool = False):
        self._widget = widget

        if enable_scrolling:
            self.__scroll = QScrollArea(self._widget)

            self._viewport = QWidget(self.__scroll)
            self.__layout = QVBoxLayout(self._viewport)
            self.__layout.setMargin(0)
            self.__layout.setSpacing(0)
            self._viewport.setLayout(self.__layout)

            self.__scroll.setWidget(self._viewport)
            self.__scroll.setWidgetResizable(True)

            self._widget.setWidget(self.__scroll)

            self.__layouts = [self.__layout]
            self._window_layout = QVBoxLayout(self._widget)
            self._window_layout.setMargin(0)
            self._window_layout.setSpacing(0)
            self._widget.setLayout(self._window_layout)
        else:
            self.__layouts = [QVBoxLayout()]
            self._widget.setLayout(self.get_current_layout())

        self._widget.setWindowTitle(title)
        self._widget.resize(0, 0)

    @abstractmethod
    def _show(self):
        """
        Internal method, that called from show()
        :return:
        """

    def show(self):
        """
        Show this window
        :return:
        """
        self._show()

    def add_widget(self, widget: Widget):
        """
        Add widget to window layout
        :param widget: Widget unit
        :return: widget instance
        """
        self.get_current_layout().addStretch()
        self.get_current_layout().addLayout(widget.get_layout())
        self.get_current_layout().addStretch()
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

    def add_subwindow(self, title: str):
        """
        Create subwindow
        :param title: window title
        :return: window
        @rtype Window
        """
        return Window(title, self._widget)

    def get_instance(self):
        return self._widget

    def insert_text_label(self, text, is_link=False):
        widget = QLabel(text)
        widget.setOpenExternalLinks(is_link)
        self.get_current_layout().addWidget(widget)

    def close(self):
        self._widget.close()


class Window(AbstractWindow):
    def __init__(self, title: str = "", parent=None):
        super().__init__(title, QDialog(parent))
        self._widget.setWindowFlags(self._widget.windowFlags() & (~Qt.WindowContextHelpButtonHint))

    def _show(self):
        self._widget.exec_()


class MainWindow(AbstractWindow):
    def __init__(self, title: str = ""):
        super().__init__(title, QWidget())

    def _show(self):
        self._widget.show()


class DockWidget(AbstractWindow):
    def __init__(self, title: str, parent):
        super().__init__(title, QDockWidget(parent), True)
        parent.addDockWidget(Qt.LeftDockWidgetArea, self._widget)
        self.__parent = parent
        self._widget.show()

    def tabify(self, dock: QDockWidget):
        """
        Align dock widget with existing
        :param dock: dock widget
        """
        self.__parent.tabifyDockWidget(dock, self._widget)

    def _show(self):
        self._widget.show()


class MessageWindow(Window):
    def __init__(self, title: str, message: str = None):
        super().__init__(title)

        if message is not None:
            self.insert_text_label(message)

        self.__btn = self.add_widget(Button("Ok")).set_on_click_callback(lambda: self.close())


class DialogWindow(Window):
    def __init__(self, title: str, buttons: [str], message: str = None):
        super().__init__(title)

        if message is not None:
            self.insert_text_label(message)

        self.__choose = None
        self.start_horizontal()
        for button in buttons:
            self.__add_method(button)
            callback = getattr(self, button)
            self.add_widget(Button(button)).set_on_click_callback(lambda: self.close()).set_on_click_callback(callback)
        self.cancel()

    def show(self):
        super().show()
        return self.__choose

    def __add_method(self, rvalue):
        def innerdynamo():
            self.__choose = rvalue

        innerdynamo.__name__ = rvalue
        setattr(self, innerdynamo.__name__, innerdynamo)


class ProgressWindow(Window):
    def __init__(self, title: str):
        super().__init__(title)

        self.__progress_bar = self.add_widget(ProgressBar())
        self.__btn = self.add_widget(Button("Cancel")).set_on_click_callback(lambda: self.close())

    def show(self):
        super().show()

    def set_value(self, value: int, status: str = ""):
        self.__progress_bar.set_value(value, status)


class DoubleProgressWindow(Window):
    def __init__(self, title: str):
        super().__init__(title)

        self.__pbar = self.add_widget(ProgressBar())
        self.__overall_pbar = self.add_widget(ProgressBar())
        self.__btn = self.add_widget(Button("Cancel")).set_on_click_callback(lambda: self.close())

    def show(self):
        super().show()

    def set_overall_value(self, value: int, status: str = ""):
        self.__pbar.set_value(value, status)

    def set_value(self, value: int, status: str = ""):
        self.__overall_pbar.set_value(value, status)
