import sys
import threading
import time  # 记录Log时间
import tkinter as tk
import tkinter.messagebox as messagebox
import types
from typing import Optional

import Source.Config as Config

showErrorEvent = threading.Event()


def showError():
    tk_ = tk.Tk()
    tk_.withdraw()
    while True:
        showErrorEvent.wait()
        messagebox.showerror("错误", "很抱歉, 出现了一些错误\n错误信息已经记录在Log.log文件中")
        showErrorEvent.clear()


def excepthook(excType, excValue, tb: Optional[types.TracebackType]):
    localTime = time.localtime()
    logTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)

    logMsg = f"{logTime}, Error Message\n"

    logMsg += excType.__name__ + "\n" + str(excValue) + "\n" + "-" * 10 + "\n"

    i = 1
    while tb:
        logMsg += f"Stack {i}\n"
        tracebackCode = tb.tb_frame.f_code
        logMsg += f"File Name: {tracebackCode.co_filename}\n"
        logMsg += f"Function or Module Name: {tracebackCode.co_name}\n"
        logMsg += f"First Line Number: {tracebackCode.co_firstlineno}\n"
        logMsg += f"Line Number: {tb.tb_lineno}\n"
        tb = tb.tb_next
        i += 1

    with open(Config.LOG_FILE_PATH, "a", encoding="utf-8") as f:  # 写入日志文件
        f.write(logMsg + "\n")

    showErrorEvent.set()


def threadingExcepthook(exceptHookArgs: threading.ExceptHookArgs):
    excepthook(exceptHookArgs.exc_type, exceptHookArgs.exc_value,
               exceptHookArgs.exc_traceback)


def init():
    if Config.IS_DEBUG_MODE:
        return
    
    thread = threading.Thread(target=showError)
    thread.setName("showErrorThread")
    thread.setDaemon(True)
    thread.start()
    sys.excepthook = excepthook
    threading.excepthook = threadingExcepthook
