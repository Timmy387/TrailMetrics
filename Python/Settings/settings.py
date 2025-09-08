import json
import customtkinter as ctk
import os
import ctypes
from Settings.sizes import Sizes


class Settings:
    def __init__(self):
        self.sizes = Sizes()
        CONFIG_DIR = os.path.join(os.getenv("APPDATA"), "TrailMetrics", "Files")
        self.CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
        self.config = None
        self.load_config()
        if self.config is None:
            print("Error loading config file.")
            exit()

        ctk.set_appearance_mode(self.theme())
        ctk.set_default_color_theme(self.color_scheme())


    def get_sizes(self):
        return self.sizes

    def screen_width(self):
        return self.config["environment"]["screenSize"]["width"]

    def screen_height(self):
        return self.config["environment"]["screenSize"]["height"]

    def scale_factor(self):
        return self.config["environment"]["scaleFactor"]

    def theme(self):
        return self.config["settings"]["theme"]

    def color_scheme(self):
        return self.config["settings"]["colorScheme"]

    def font(self):
        return self.config["settings"]["font"]

    def window_scale(self):
        return self.config["settings"]["windowScale"]

    def width(self):
        if self.config["settings"]["useScale"]:
            return self.sizes.width
        return self.config["settings"]["lastSize"]["width"]

    def height(self):
        if self.config["settings"]["useScale"]:
            return self.sizes.height
        return self.config["settings"]["lastSize"]["height"]

    def x(self):
        if self.config["settings"]["useScale"]:
            return self.sizes.x
        return int(self.config["settings"]["lastPosition"]["x"] * self.scale_factor())

    def y(self):
        if self.config["settings"]["useScale"]:
            return self.sizes.y
        return int(self.config["settings"]["lastPosition"]["y"] * self.scale_factor())

    def use_scale(self):
        return self.config["settings"]["useScale"]

    def total_or_avg(self):
        return self.config["settings"]["graphSettings"]["totalOrAvg"]

    def cmp_trails_or_dates(self):
        return self.config["settings"]["graphSettings"]["cmpTrailsOrDates"]

    def legend(self):
        return self.config["settings"]["graphSettings"]["legend"]

    def grid(self):
        return self.config["settings"]["graphSettings"]["grid"]

    def graph_type(self):
        return self.config["settings"]["graphSettings"]["graphType"]

    def zoom_graph(self):
        return self.config["settings"]["graphSettings"]["zoomGraph"]


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


    def get_defaults(self):
        return self.config["defaults"]


def build_config(screenWidth, screenHeight):
    # CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    sf = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    config = None
    CONFIG_DIR = os.path.join(os.getenv("APPDATA"), "TrailMetrics", "Files")
    os.makedirs(CONFIG_DIR, exist_ok=True)
    CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as file:
            config = {"settings": {

                    },

                    "defaults": {
                        "theme": "Light",
                        "colorScheme": "dark-blue",
                        "font": "Roboto",
                        "windowScale": 0.7,
                        "lastSize": {
                            "width": int(screenWidth * 0.7),
                            "height": int(screenHeight * 0.7)},
                        "lastPosition": {
                            "x": int(screenWidth // 2 - screenWidth * 0.7 // 2),
                            "y": int(screenHeight // 2 - screenHeight * 0.7 // 2 - 50)},
                        "useScale": True,
                        "graphSettings": {
                            "totalOrAvg": 1,
                            "cmpTrailsOrDates": 1,
                            "legend": True,
                            "grid": True,
                            "graphType": "Line",
                            "zoomGraph": False
                        }
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
    CONFIG_DIR = os.path.join(os.getenv("APPDATA"), "TrailMetrics", "Files")
    CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
    with open(CONFIG_PATH) as file:
        config = json.load(file)
        config["settings"] = config["defaults"]
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)
    return config