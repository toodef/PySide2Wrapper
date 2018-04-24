from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, \
    QComboBox, QProgressBar
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtCore import QObject
from abc import ABCMeta, abstractmethod


class Checkable(metaclass=ABCMeta):
    @abstractmethod
    def add_clicked_callback(self, callback: callable):
        """
        Add callback, that will call for every click
        :param callback: callback
        :return: Widget object
        :rtype: Widget
        """

    @abstractmethod
    def get_value(self):
        """
        Get state of Widget: checked or not
        :return: State
        :rtype: bool
        """


class Widget:
    def __init__(self, instance: QObject):
        self._layout = None
        self._instance = instance
        self._enabled_dependencies = []

    def get_layout(self):
        """
        Return layout of widget
        :return: layout, contains Widget instance
        @:rtype: QLayout
        """
        return self._layout

    def get_instance(self):
        """
        Get Qt instance of widget
        :return: instance of widget (PySide object)
        :rtype QWidget
        """
        return self._instance

    def set_enabled(self, is_enabled: bool = True):
        """
        Set widget enabled
        :param is_enabled: state of widget: enabled or not
        :return: Widget object (self)
        :rtype: Widget
        """
        if is_enabled:
            for depends in self._enabled_dependencies:
                if not depends.get_value():
                    self._instance.setEnabled(False)
                    return self
        self._instance.setEnabled(is_enabled)
        return self

    def add_enabled_dependency(self, dependency: Checkable):
        self.set_enabled(dependency.get_value())
        self._enabled_dependencies.append(dependency)
        dependency.add_clicked_callback(self.set_enabled)


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
        return self._instance.text()

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


class CheckBox(Widget, Checkable):
    def __init__(self, title: str):
        super().__init__(QCheckBox(title))
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._instance)

    def add_clicked_callback(self, callback: callable):
        self._instance.toggled.connect(callback)
        return self

    def get_value(self):
        return self._instance.isChecked()


class RadioButton(Widget, Checkable):
    def __init__(self, title: str):
        super().__init__(QRadioButton(title))
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._instance)

    def get_value(self):
        return self._instance.isChecked()

    def add_clicked_callback(self, callback: callable):
        self._instance.toggled.connect(callback)
        return self


class ComboBox(LabeledWidget, ValueContains):
    def __init__(self):
        super().__init__(QComboBox())

    def _assembly(self):
        if self._layout is None:
            self._layout = QVBoxLayout()
            self._layout.addWidget(self._instance)

    def add_items(self, values: []):
        """
        Add values to combo box
        @param values: list of values
        @return: self instance
        """
        for v in values:
            self._instance.addItem(v)

        return self

    def set_value(self, value: int):
        self._instance.setCurrentIndex(value)

    def get_value(self):
        return self._instance.currentIndex()


class ProgressBar(Widget, ValueContains):
    def __init__(self):
        super().__init__(QProgressBar())
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._instance)

    def set_value(self, value: int):
        self._instance.setValue(value)

    def get_value(self):
        return self._instance.getValue()
