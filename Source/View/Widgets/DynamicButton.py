from enum import Enum

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize

from Source.View.Utils.WidgetAnimationHelper import WidgetAnimationHelper


class DynamicButtonTransformMode(Enum):
    Size = 0
    Width = 1
    Height = 2

class DynamicButton(QPushButton):
    def __init__(self):
        super().__init__()

        self.oriSize = QSize(60, 60)
        self.hoverSize = QSize(120, 60)
        self.animDurationSecond = 0.6
        self.mode = DynamicButtonTransformMode.Size
        self.animHelper = WidgetAnimationHelper(self)

    def enterEvent(self, event) -> None:
        if self.mode == DynamicButtonTransformMode.Size:
            self.animHelper.setFixedSize(self.hoverSize, self.animDurationSecond)
        elif self.mode == DynamicButtonTransformMode.Width:
            self.animHelper.setWidth(self.hoverSize.width(), self.animDurationSecond)
        elif self.mode == DynamicButtonTransformMode.Height:
            self.animHelper.setHeight(self.hoverSize.height(), self.animDurationSecond)

        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        if self.mode == DynamicButtonTransformMode.Size:
            self.animHelper.setFixedSize(self.oriSize, self.animDurationSecond)
        elif self.mode == DynamicButtonTransformMode.Width:
            self.animHelper.setWidth(self.oriSize.width(), self.animDurationSecond)
        elif self.mode == DynamicButtonTransformMode.Height:
            self.animHelper.setHeight(self.oriSize.height(), self.animDurationSecond)

        return super().leaveEvent(event)