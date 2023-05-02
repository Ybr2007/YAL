import typing
from Source.View.Interfaces.BaseInterface import BaseInterface


T = typing.TypeVar("T", bound=BaseInterface)

class InstanceHelper:
    def __init__(self):
        raise RuntimeError("Helper不应被实例化")
    
    @staticmethod
    def getApp():
        from Source.App import App

        return App()  # type: ignore
    
    @staticmethod
    def getMainWindow():
        return InstanceHelper.getApp().mainWindow
    
    @staticmethod
    def getCurInterface(interfaceType: typing.Optional[typing.Type[T]]=None) -> typing.Optional[T]:
        curInterface = InstanceHelper.getMainWindow().curInterface

        if interfaceType is None:
            return curInterface
        
        if isinstance(curInterface, interfaceType):
            return curInterface
        
        return None