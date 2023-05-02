import threading

from ..IProcedure import IProcedure
from Source.View.Interfaces import MainInterface
from Source.App import App


class MainHomeProcedure(IProcedure):
    def onEnter(self):
        App().mainWindow.changeInterfaceTo(MainInterface())

    def onExit(self):
        ...