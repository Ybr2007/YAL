import typing

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Source.View.FramelessWindow import FramelessWindow
import Source.Data.UserData as UserData
from Source.View.Utils import *
from Source.View.Interfaces import BaseInterface
import Source.Info as Info


class MainWindow(FramelessWindow):
    """
    主窗口
    """

    def __init__(self):
        super().__init__()

        self.initWindow()  # 初始化窗口
        self.initUI()  # 初始化界面
        self.initLogic()  # 初始化逻辑

    def initWindow(self):
        """初始化窗口"""
        self.setGeometry(*UserData.getWindowGeometry())  # 跨会话恢复窗口位置和尺寸
        self.setWindowTitle(Info.ApplicationName)
        self.setWindowIcon(QIcon(":/Icons/Logo.svg"))

    def initUI(self):
        """初始化界面"""
        self.titleBar.setFixedHeight(48)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.mainLayout.setSpacing(0)

        self.titleBar.titleLabel
        
        self.curInterface = None

        self.titleBar.raise_()

    def initLogic(self):
        """初始化逻辑"""
        ...

    def changeInterfaceTo(self, interface: typing.Optional[BaseInterface]):
        if self.curInterface:
            def removeOldInterfaceCallback(oldInterface: BaseInterface, newInterface: BaseInterface):
                self.mainLayout.removeWidget(oldInterface)
                oldInterface.hide()
                oldInterface.deleteLater()

                self.mainLayout.addWidget(newInterface)

            # 当这个回调被调用时self.interface已经改变
            # 因此使用lambda默认参数时传入removeOldInterfaceCallback是正确的值
            self.curInterface.onExit(
                lambda oldInterface=self.curInterface:
                    removeOldInterfaceCallback(oldInterface, interface)
            )
        elif interface:
            self.mainLayout.addWidget(interface)

        self.curInterface = interface

        if self.curInterface:
            self.curInterface.onEnter()

    def closeEvent(self, event: QCloseEvent) -> None:
        if not self.isMaximized():
            UserData.userData["window_geometry"] = {
                "x": self.geometry().x(),
                "y": self.geometry().y(),
                "width": self.geometry().width(),
                "height": self.geometry().height(),
                "is_maximizd": False
            }
        else:
            UserData.userData["window_geometry"]["is_maximizd"] = True

        return super().closeEvent(event)
