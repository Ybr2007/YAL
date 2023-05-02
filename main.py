if __name__ == "__main__":
    import Source.Debug.ErrorCather as ErrorCather
    ErrorCather.init()

    from Source.Manager.ProcedureManager import ProcedureManager
    from Source.Procedure.Procedures import StartupProcedure   

    ProcedureManager.changeProcedureTo(StartupProcedure())