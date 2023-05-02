import Source.Config as Config

if Config.IS_DEBUG_MODE:
    with open("Assets/Theme/Dark.qss", "r") as f:
        dark = f.read()

else:
    dark = ""  # 将qss内容复制到此处