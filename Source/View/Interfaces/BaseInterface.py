import typing

from PyQt5.QtWidgets import QWidget


class BaseInterface(QWidget):
    def __init__(self, parent: typing.Optional[QWidget]=None):
        super().__init__(parent)

        self.initUI()
        self.initLogic()

    def initUI(self):
        ...

    def initLogic(self):
        ...

    def onEnter(self):
        ...

    def onExit(self, finishSwitch: typing.Callable):
        finishSwitch()