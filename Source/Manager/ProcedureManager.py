import typing

from Source.Procedure import IProcedure


class ProcedureManager:
    __curProcedure: typing.Optional[IProcedure] = None

    def __init__(self): 
        raise Exception("Manager不应被实例化")

    @classmethod
    def changeProcedureTo(cls, state: typing.Optional[IProcedure]):
        if cls.__curProcedure:
            cls.__curProcedure.onExit()

        cls.__curProcedure = state

        if cls.__curProcedure:
            cls.__curProcedure.onEnter()
            