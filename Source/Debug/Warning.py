import time

import Source.Config as Config


def _warn(message: str, printToConsole: bool=True, outputToFile: bool=True):
    if printToConsole:
        print(f"\033[33m警告: {message}\033[0m")
    if outputToFile:
        localTime = time.localtime()
        logTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)

        logMsg = f"{logTime}, Warning Message\n" + message + "\n"

        with open(Config.LOG_FILE_PATH, "a", encoding="utf-8") as f:  # 写入日志文件
            f.write(logMsg + "\n")

def warn(message: str):
    if Config.IS_DEBUG_MODE:
        _warn(message)
    else:
        _warn(message, False)