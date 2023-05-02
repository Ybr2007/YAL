from ..IProcedure import IProcedure
from .MainHomeProcedure import MainHomeProcedure
from .FinalProcedure import FinalProcedure


class StartupProcedure(IProcedure):
    def onEnter(self):
        import sys

        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt

        from Source.App import App
        import Source.Data.UserData as UserData
        from Source.Manager.PuginManager import PluginManager
        import Source.Asset.Assets  # import后自动初始化
        from Source.Manager.ProcedureManager import ProcedureManager

        def initQt():
            QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

        initQt()

        UserData.init() 
        PluginManager.loadPlugins()
        PluginManager.call("onLoad")

        qApp = QApplication(sys.argv)
        App(qApp)

        PluginManager.call("init")

        ProcedureManager.changeProcedureTo(MainHomeProcedure())

        qApp.exec()

        ProcedureManager.changeProcedureTo(FinalProcedure())

    def onExit(self):
        ...