import os
import json
import importlib.util
import typing

import Source.Config as Config
import Source.Debug.Warning as Warning


class PluginManager:
    plugins: dict[str, dict[str, typing.Callable]] = {}

    def __init__(self):
        raise Exception("Manager不应被实例化")

    @classmethod
    def loadPlugins(cls):
        for root, dirs, files in os.walk(Config.PLUGINS_ROOT_DIR):
            for file in files:
                if file == "plugin.json":
                    readStream = open(os.path.join(root, file), "r", encoding="utf-8")
                    pluginJson = json.load(readStream)
                    pluginFile = pluginJson["pluginFile"]
                    cls.loadPlugin(os.path.join(root, pluginFile),pluginJson["pluginName"])
                    readStream.close()

    @classmethod
    def loadPlugin(cls, pluginPath, pluginName="plugin"):
        spec = importlib.util.spec_from_file_location(pluginName, pluginPath)

        if spec is None:
            return
        
        moudle = importlib.util.module_from_spec(spec)

        if spec.loader is None:
            Warning.warn(f"插件{pluginName}({pluginPath}) 加载失败")
            return
        
        spec.loader.exec_module(moudle)

        pluginFuncDict = {}

        # register plugin magic functions
        if hasattr(moudle, "onLoad") and callable(moudle.onLoad):
            pluginFuncDict["onLoad"] = moudle.onLoad
        if hasattr(moudle, "init") and callable(moudle.init):
            pluginFuncDict["init"] = moudle.init

        cls.plugins[pluginName] = pluginFuncDict

    @classmethod
    def call(cls, funcName: str, pluginName=None):
        if pluginName is None:
            for pluginName in cls.plugins:
                cls.call(funcName, pluginName)
        elif funcName in cls.plugins[pluginName]:
            cls.plugins[pluginName][funcName]()

    @classmethod
    def getPluginNames(cls) -> list[str]:
        return [pluginName for pluginName in cls.plugins]
