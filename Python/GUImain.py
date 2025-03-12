import customtkinter as ctk
from GUI2.Screens.startScreen import StartScreen
from Settings.settings import Settings, build_config, load_defaults


class GUIMain(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set up settings
        build_config(self.winfo_screenwidth(), self.winfo_screenheight())
        self.settings = Settings()

        self.sizes = self.settings.sizes
        self.title("Trail Metrics")
        if self.settings.useScale:
            self.geometry(f"{self.settings.width}x{self.settings.height}+{self.settings.winX}+{self.settings.winY}")
        else:
            self.geometry(f"{self.settings.lastWidth}x{self.settings.lastHeight}+"
                          f"{self.settings.lastX}+{self.settings.lastY}")
        self.minsize(int(self.settings.width * 0.7), int(self.settings.height * 0.7))
        self.settings.update_config("settings", "useScale", False)
        self.current_frame = None
        self.switch_frame(StartScreen)
        self.protocol("WM_DELETE_WINDOW", self.close_all)
        self.mainloop()


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand = True, pady=self.sizes.pady * 2, padx=self.sizes.padx)

    def close_all(self):
        sf = self.settings.scaleFactor
        w = self.winfo_width() // sf
        h = self.winfo_height() // sf

        if w < self.settings.screenWidth and h < self.settings.screenHeight:
            self.settings.update_config("settings", "lastSize",{"width": int(w), "height": int(h)})
            self.settings.update_config("settings", "lastPosition",
                                        {"x": int(self.winfo_x()), "y": int(self.winfo_y())})
        self.destroy()


    def get_settings(self):
        return self.settings


    def get_sizes(self):
        return self.sizes


    def refresh_scheme(self):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    # if isinstance(child, ctk.CTkLabel):
                    #     child.configure(fg_color=self.settings.colorScheme)
                    if isinstance(child, ctk.CTkButton):
                        child.configure(fg_color=self.settings.colorScheme)
                        child.configure(bg_color=self.settings.colorScheme)
                    elif isinstance(child, ctk.CTkOptionMenu):
                        child.configure(fg_color=self.settings.colorScheme)
                    elif isinstance(child, ctk.CTkEntry):
                        child.configure(fg_color=self.settings.colorScheme)
            # elif isinstance(widget, ctk.CTkButton):
            #     widget.configure(fg_color=self.settings.colorScheme)
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=self.settings.colorScheme)
                widget.configure(bg_color=self.settings.colorScheme)



if __name__ == "__main__":
    GUIMain()