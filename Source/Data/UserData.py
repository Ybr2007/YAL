import os
import json

import Source.Config as Config
import Source.Info as Info


userData = {}

def init():
    global userData

    if not os.path.exists(Config.USER_DATA_FILE_PATH):
        userData = {
            "meta": {
                "version": Info.VERSION
            },
            "window_geometry": {
                "x": 100,
                "y": 100,
                "width": 800,
                "height": 600,
                "is_maximizd": False
            }
        }
    else:
        with open(Config.USER_DATA_FILE_PATH, "r", encoding="utf-8") as f:
            userData = json.load(f)

def save():
    with open(Config.USER_DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(userData, f, indent=4, ensure_ascii=False)

def getWindowGeometry() -> tuple[int, int, int, int]:
    """获取上个会话保存的窗口位置与尺寸

    Returns:
        tuple[int, int, int, int]: 位置与尺寸(x, y, width, height)
    """
    return (
        userData["window_geometry"]["x"], userData["window_geometry"]["y"],
        userData["window_geometry"]["width"], userData["window_geometry"]["height"]
    )