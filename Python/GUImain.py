import customtkinter as ctk
from GUI.Screens.startScreen import StartScreen
from Settings.settings import Settings, build_config
from connect_sqlite import connect_trail_db_sqlite
from GUI.Screens.editTrails import EditTrails
from GUI.Screens.settingsPopup import SettingsPopup
from GUI.Screens.importDataPopup import ImportData
import matplotlib.pyplot as plt
import sys

reopen_app = True
def main():
    global reopen_app
    reopen_app = True
    while reopen_app:
        GUIMain()
    sys.exit()

class GUIMain(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set up settings
        build_config(self.winfo_screenwidth(), self.winfo_screenheight())
        self.settings = Settings()

        self.sizes = self.settings.get_sizes()
        with connect_trail_db_sqlite() as conn:
            self.conn = conn
        self.title("Trail Metrics")
        self.geometry(f"{self.settings.width()}x{self.settings.height()}+{self.settings.x()}+{self.settings.y()}")
        self.minsize(int(self.sizes.width * 1), int(self.sizes.height * 0.8))
        self.settings.update_config("settings", "useScale", False)
        self.currentFrame = StartScreen(self)
        self.currentFrame.pack(fill="both", expand=True, pady=self.sizes.pady, padx=self.sizes.padx // 2)
        # self.switch_frame(StartScreen)
        self.protocol("WM_DELETE_WINDOW", self.close_all)
        self.bind("<Button-1>", self.click)
        # bind shortcuts
        self.bind("<Control-d>", lambda e: self.currentFrame.build_graphs())
        self.bind("<Control-s>", lambda e: self.currentFrame.save_graph())
        self.bind("<Control-u>", lambda event: self.currentFrame.open_popup(ImportData))
        self.bind("<Control-e>", lambda event: self.currentFrame.open_popup(EditTrails))
        self.bind("<Control-Shift-S>", lambda event: self.currentFrame.open_popup(SettingsPopup))
        self.bind("<Control-c>", lambda e: self.currentFrame.clear_config())
        self.bind("<Control-h>", lambda e: self.currentFrame.help())
        self.bind("<Control-q>", lambda e: self.close_all(reopen=False))
        self.mainloop()


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.currentFrame is not None:
            self.currentFrame.destroy()
        self.currentFrame = new_frame
        self.currentFrame.pack(fill="both", expand=True, pady=self.sizes.pady, padx=self.sizes.padx // 2)

    def close_all(self, reopen=False):
        sf = self.settings.scale_factor()
        w = self.winfo_width() // sf
        h = self.winfo_height() // sf
        x = int(self.winfo_x() // sf)
        y = int(self.winfo_y() // sf)

        if w < self.settings.screen_width() and h < self.settings.screen_height():
            self.settings.update_config("settings", "lastSize",{"width": int(w), "height": int(h)})
            self.settings.update_config("settings", "lastPosition",
                                        {"x": x, "y": y})
        self.destroy()
        for event_id in self.tk.eval('after info').split():
            try:
                self.after_cancel(event_id)
            except Exception:
                pass
        self.conn.close()
        plt.close('all')
        global reopen_app
        reopen_app = reopen


    def get_settings(self):
        return self.settings


    def get_sizes(self):
        return self.sizes


    def get_conn(self):
        return self.conn


    def refresh_scheme(self):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    # if isinstance(child, ctk.CTkLabel):
                    #     child.configure(fg_color=self.settings.colorScheme)
                    if isinstance(child, ctk.CTkButton):
                        child.configure(fg_color=self.settings.color_scheme())
                        child.configure(bg_color=self.settings.color_scheme())
                    elif isinstance(child, ctk.CTkOptionMenu):
                        child.configure(fg_color=self.settings.color_scheme())
                    elif isinstance(child, ctk.CTkEntry):
                        child.configure(fg_color=self.settings.color_scheme())
            # elif isinstance(widget, ctk.CTkButton):
            #     widget.configure(fg_color=self.settings.color_scheme())
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=self.settings.color_scheme())
                widget.configure(bg_color=self.settings.color_scheme())

    def current_x(self):
        return int(self.winfo_x() // self.settings.scale_factor())

    def current_y(self):
        return int(self.winfo_y() // self.settings.scale_factor())

    def current_location(self):
        tup = self.current_x(), self.current_y()
        return tup

    def click(self, event=None):
        self.currentFrame.click(event)


if __name__ == "__main__":
    main()