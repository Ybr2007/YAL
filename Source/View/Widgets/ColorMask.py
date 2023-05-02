import typing

from PyQt5.QtWidgets import QHBoxLayout, QWidget
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QPainter, QColor, QResizeEvent


class ColorMask(QWidget):
    def __init__(self, parent: typing.Optional[QWidget]=None):
        super().__init__()

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(100, 120, 100, 120)
        
        self.color = QColor(0, 0, 0, 175)
        
        self.move(0, 0)
        self.setParent(parent)

    def setParent(self, parent: typing.Optional[QWidget]=None):  # type: ignore
        if parent is not None:
            parent.installEventFilter(self)
            self.setFixedSize(parent.size())
        super().setParent(parent)  # type: ignore

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.color)
        return super().paintEvent(event)
    
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is self.parent():
            if isinstance(event, QResizeEvent):
                self.setFixedSize(event.size())

        return super().eventFilter(obj, event)
    