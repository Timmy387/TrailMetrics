import json
import os


class Sizes:
    def __init__(self):
        CONFIG_DIR = os.path.join(os.getenv("APPDATA"), "TrailMetrics", "Files")
        self.CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
        self.config = self.open_json()

        self.screenWidth: int = self.config["environment"]["screenSize"]["width"]
        self.screenHeight: int = self.config["environment"]["screenSize"]["height"]
        self.scale: float = self.config["settings"]["windowScale"]
        self.font: str = self.config["settings"]["font"]
        self.width: int = int(self.screenWidth * self.scale)
        self.height: int = int(self.screenHeight * self.scale)
        self.x: int = int(self.screenWidth // 2 - self.width // 2)
        self.y: int = int(self.screenHeight // 2 - self.height // 2 - 30)
        self.base_font_size: int = int(self.width // 30)
        self.font1_8: tuple = (self.font, int(self.base_font_size // 8))
        self.font2_8: tuple = (self.font, self.font1_8[1] * 2)
        self.font3_8: tuple = (self.font, self.font1_8[1] * 3)
        self.font4_8: tuple = (self.font, self.font1_8[1] * 4)
        self.font5_8: tuple = (self.font, self.font1_8[1] * 5)
        self.font6_8: tuple = (self.font, self.font1_8[1] * 6)
        self.font7_8: tuple = (self.font, self.font1_8[1] * 7)
        self.font_full = (self.font, self.base_font_size)
        self.new_window_width: int = int(self.width * 0.55)
        self.new_window_height: int = int(self.height * 0.82)
        self.new_window_x: int = int(self.screenWidth // 2 - self.new_window_width // 3)
        self.new_window_y: int = int(self.screenHeight // 2 - self.new_window_height // 2)
        self.pady: int = int(self.height * 0.01)
        self.padx: int = int(self.width * 0.01)
        self.pady_title: int = int(self.height * 0.05)


    def open_json(self):
        with open(self.CONFIG_PATH) as file:
            self.config = json.load(file)
        return self.config