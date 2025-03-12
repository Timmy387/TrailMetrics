import customtkinter as ctk


class Popup(ctk.CTkToplevel):
    def __init__(self, master,
                 title="Window", text="",
                 width: int=200, height: int=100,
                 x: int=None, y: int=None):
        super().__init__(master)
        self.width = width
        self.height = height
        self.geometry(f"{width}x{height}+500+400")
        if x is not None and y is not None:
            self.geometry(f"{height}x{width}+{x}+{y}")
        self.title(title)

        self.success = ctk.CTkLabel(master=self, text=text,
                               text_color="white", font=("Roboto", 30))
        self.success.pack(pady=17)

        self.close_button = ctk.CTkButton(master=self, text="Close", command=self.destroy)
        self.close_button.pack(pady=10)

        self.bind("<Return>", self.close)
        # bind escape key to close the window
        self.bind("<Escape>", self.close)
        self.attributes("-topmost", True)
        # make sure window cant be made too much smaller
        self.resizable(False, False)
        self.focus()


    def change_text(self, new_text: str=""):
        self.success.configure(text=new_text)


    def center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.width) + 17
        y = (self.winfo_screenheight() // 2) - (self.height) + 15

        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.focus_set()
        self.grab_set()


    def close(self, event):
        self.destroy()