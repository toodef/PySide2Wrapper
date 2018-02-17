from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtCore import QObject, QRect
from abc import ABCMeta, abstractmethod


class Widget:
    def __init__(self, instance: QObject):
        self._layout = None
        self._instance = instance

    def get_layout(self):
        """
        Return layout of widget
        :return: layout
        @:rtype: QLayout
        """
        return self._layout

    def get_instance(self):
        """
        Get Qt instance of widget
        :return:
        """
        return self._instance


class LabeledWidget(Widget, metaclass=ABCMeta):
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

    def get_layout(self):
        """
        Return layout of widget
        :return: layout
        @:rtype: QLayout
        """
        self._assembly()
        return self._layout

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


class LineEdit(LabeledWidget, ValueContains):
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


class Button(Widget):
    def __init__(self, title: str):
        super().__init__(QPushButton())
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._instance)
        self._instance.setText(title)

    def set_on_click_callback(self, callback: callable):
        """
        Set callback on click event
        :param callback:
        :return:
        """
        self._instance.clicked.connect(callback)
        return self


class ImageLayout(Widget):
    def __init__(self):
        super().__init__(QLabel())
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._instance)
        self.__pixmap = None

    def set_image_from_data(self, image, width, height, bytes_per_line):
        img = QImage(image, width, height, bytes_per_line, QImage.Format_RGB888)
        self.__pixmap = QPixmap.fromImage(img)
        self._instance.setPixmap(self.__pixmap)
        return self

    def set_image_from_file(self, file_path: str):
        self._instance.setPixmap(file_path)
        return self

    def set_size(self, width, height):
        self.__pixmap = self.__pixmap.scaledToWidth(width).scaledToHeight(height)
        self._instance.setPixmap(self.__pixmap)
        return self

    def get_size(self):
        return self.__pixmap.width(), self.__pixmap.height()
