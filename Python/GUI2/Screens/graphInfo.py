import customtkinter as ctk

class GraphInfo(ctk.CTkFrame):
    def __init__(self, master, num_frames):
        super().__init__(master)
        self.sizes = master.get_sizes()

