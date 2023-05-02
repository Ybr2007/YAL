from PyQt5.QtWidgets import QApplication

from Source.View.MainWindow import MainWindow
import Source.Asset.Theme as Theme
import Source.Data.UserData as UserData
from Source.Utils.Singleton import singleton


@singleton
class App:
    def __init__(self, app: QApplication):
        self.app = app
        self.app.setStyleSheet(Theme.dark)

        self.mainWindow = MainWindow()

        if UserData.userData["window_geometry"]["is_maximizd"]:
            self.mainWindow.showMaximized()
        else:
            self.mainWindow.show()
