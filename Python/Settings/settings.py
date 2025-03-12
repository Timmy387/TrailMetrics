import json
import customtkinter as ctk
import os
import ctypes
from Settings.sizes import Sizes


class Settings:
    def __init__(self):
        self.sizes = Sizes()
        self.CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.config = None
        self.load_config()
        if self.config is None:
            print("Error loading config file.")
            exit()

        self.screenWidth = self.config["environment"]["screenSize"]["width"]
        self.screenHeight = self.config["environment"]["screenSize"]["height"]
        self.scaleFactor = self.config["environment"]["scaleFactor"]

        self.theme = self.config["settings"]["theme"]
        ctk.set_appearance_mode(self.theme)
        self.colorScheme = self.config["settings"]["colorScheme"]
        ctk.set_default_color_theme(self.colorScheme)

        self.font = self.config["settings"]["font"]
        self.windowScale = self.config["settings"]["windowScale"]

        self.width = self.sizes.width
        self.height = self.sizes.height
        self.winX = self.sizes.x
        self.winY = self.sizes.y

        self.lastWidth = int(self.config["settings"]["lastSize"]["width"])
        self.lastHeight = int(self.config["settings"]["lastSize"]["height"])
        self.lastX = int(self.config["settings"]["lastPosition"]["x"])
        self.lastY = int(self.config["settings"]["lastPosition"]["y"])

        self.useScale = self.config["settings"]["useScale"]


    def save_config(self):
        with open(self.CONFIG_PATH, "w") as file:
            json.dump(self.config, file, indent=4)


    def update_config(self, section, key, value):
        self.config[section][key] = value
        self.save_config()


    def load_config(self):
        with open(self.CONFIG_PATH) as file:
            self.config = json.load(file)


    def back_to_defaults(self):
        self.config = load_defaults()
        self.theme = self.config["settings"]["theme"]
        self.colorScheme = self.config["settings"]["colorScheme"]
        self.font = self.config["settings"]["font"]
        self.windowScale = self.config["settings"]["windowScale"]
        self.useScale = self.config["settings"]["useScale"]


    def get_defaults(self):
        return self.config["defaults"]



def build_config(screenWidth, screenHeight):
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    sf = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    config = None
    if os.path.exists(CONFIG_PATH):
        return
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as file:
            config = {"settings": {

                    },

                    "defaults": {
                        "theme": "System",
                        "colorScheme": "green",
                        "font": "Roboto",
                        "windowScale": 0.7,
                        "lastSize": {
                            "width": int(screenWidth * 0.7),
                            "height": int(screenHeight * 0.7)},
                        "lastPosition": {
                            "x": int(screenWidth // 2 - screenWidth * 0.7 // 2),
                            "y": int(screenHeight // 2 - screenHeight * 0.7 // 2 - 50)},
                        "useScale": True
                    },

                "environment": {
                    "screenSize":
                        {"width": int(screenWidth),
                         "height": int(screenHeight)},
                    "scaleFactor": sf
                }
            }
            json.dump(config, file, indent=4)
    if config:
        load_defaults()


def load_defaults():
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    with open(CONFIG_PATH) as file:
        config = json.load(file)
        config["settings"] = config["defaults"]
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)
    return config