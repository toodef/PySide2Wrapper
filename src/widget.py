from PySide2.QtWidgets import QLineEdit, QVBoxLayout, QHBoxLayout, QLabel
from PySide2.QtCore import QObject
from abc import ABCMeta, abstractmethod


class Widget(metaclass=ABCMeta):
    def __init__(self, instance: QObject):
        self._layout = None
        self._instance = instance

    def get_layout(self):
        """
        Return layout of widget
        :return: layout
        @:rtype: QLayout
        """
        self._assembly()
        return self._layout

    def get_instance(self):
        """
        Get Qt instance of widget
        :return:
        """
        return self._instance

    def add_label(self, text: str, position: str):
        """
        Add label to widget
        :param text: label text
        :param position: position of label ['top', 'left', 'right', 'bottom']
        :return: self value
        """
        if not (position in ['top', 'bottom', 'left', 'right']):
            raise Exception("Wrong position for label: " + text)

        if position in ['top', 'bottom']:
            self._layout = QVBoxLayout()
        elif position in ['left', 'right']:
            self._layout = QHBoxLayout()

        if position in ['top', 'left']:
            self._layout.addWidget(QLabel(text))
            self._layout.addWidget(self._instance)
        elif position in ['bottom', 'right']:
            self._layout.addWidget(self._instance)
            self._layout.addWidget(QLabel(text))

        return self

    @abstractmethod
    def _assembly(self):
        """
        Assembly object
        :return: object instance
        """


class ValueContains(metaclass=ABCMeta):
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


class LineEdit(Widget, ValueContains):
    def __init__(self):
        super().__init__(QLineEdit())

    def set_value(self, value: str):
        """
        Set value to
        :param value:
        :return:
        """
        self._instance.setText(value)

    def get_value(self):
        """
        Get current value
        :return: current value
        """
        self._instance.text()

    def _assembly(self):
        if self._layout is None:
            self._layout = QVBoxLayout()
            self._layout.addWidget(self._instance)
