from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .BaseInterface import BaseInterface


class MainInterface(BaseInterface):
    def initUI(self) -> None:
        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.addWidget(
            label := QLabel("<p style='font-size:40pt'>YApplication Framework</p>"), Qt.AlignmentFlag.AlignCenter)
        
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)