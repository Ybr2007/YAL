from ..IProcedure import IProcedure


class FinalProcedure(IProcedure):
    def onEnter(self):
        import os
        import Source.Data.UserData as UserData

        UserData.save()
        os._exit(0)  # 程序彻底退出

    def onExit(self):
        ...