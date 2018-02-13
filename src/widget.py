from PySide2.QtWidgets import QLineEdit
from abc import ABCMeta, abstractmethod


class Widget(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def get_instance(self):
        """
        Get Qt instance of widget
        :return:
        """


class ValueContains(Widget, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def set_value(self, value):
        """
        Set value to
        :param value: value to set
        :return: None
        """

    @abstractmethod
    def get_value(self):
        """
        Get value
        :return: current value
        """


class LineEdit(Widget):
    def __init__(self):
        super().__init__()
        self.__line_edit = QLineEdit()

    def set_value(self, value):
        """
        Set value to
        :param value:
        :return:
        """
        pass

    def get_value(self):
        """
        Get current value
        :return: current value
        """
        pass

