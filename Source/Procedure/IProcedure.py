from abc import ABCMeta, abstractclassmethod


class IProcedure(metaclass=ABCMeta):
    @abstractclassmethod
    def onEnter(self):
        ...

    @abstractclassmethod
    def onExit(self):
        ...