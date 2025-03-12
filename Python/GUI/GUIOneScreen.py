import customtkinter as ctk
from Screens.startScreen import StartScreen

class MainGUI(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.title("Trail Metrics")
        self.geometry("1000x700+50+50")
        self.current_frame = None
        self.minsize(700, 550)
        self.switch_frame(StartScreen)


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand = True, pady=15, padx=15)


    def rtn(self):
        self.switch_frame(StartScreen)



if __name__ == "__main__":
    MainGUI().mainloop()