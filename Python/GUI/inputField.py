import customtkinter as ctk

class InputField(ctk.CTkFrame):
    def __init__(self, master, label_text, placeholder_text):
        super().__init__(master)
        self.configure(bg_color="transparent")

        self.label = ctk.CTkLabel(master=self, text=label_text, font=("Roboto", 20))
        self.label.pack(pady=2)

        self.input = ctk.CTkEntry(master=self, font=("Roboto", 35), placeholder_text=placeholder_text, width=300)
        self.input.pack()


