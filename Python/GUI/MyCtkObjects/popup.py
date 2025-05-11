import customtkinter as ctk


class Popup(ctk.CTkToplevel):
    def __init__(self, master,
                 title="Window", text="",
                 width: int=300, height: int=110,
                 x: int=None, y: int=None, yesno: bool=False, yes: str="Yes", no: str="No"):
        super().__init__(master)
        self.sizes = master.get_sizes()
        self.width = width
        self.height = text.count("\n") * 15 + height + self.sizes.pady * 4
        self.x = self.sizes.screenWidth // 2
        self.y = self.sizes.screenHeight // 2 - height // 2
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        if x is not None and y is not None:
            self.geometry(f"{height}x{width}+{x}+{y}")
        self.title(title)

        self.success = ctk.CTkLabel(master=self, text=text, font=self.sizes.font5_8)
        self.success.pack(pady=self.sizes.pady * 2)

        self.yesBtn = None
        self.noBtn = None
        self.close_button = None
        self.buttonFrame = None
        self.ans = False
        self.yes = yes
        self.no = no
        if yesno:
            self.build_yesno()
        else:
            self.close_button = ctk.CTkButton(master=self, text="Close", command=self.close,
                                          font=self.sizes.font4_8)
            self.configure(width=self.close_button.winfo_width() // 2)
            self.close_button.pack()
            self.bind("<Return>", self.close)
        # bind escape key to close the window
        self.bind("<Escape>", self.close)
        self.attributes("-topmost", True)
        # make sure window cant be made too much smaller
        self.resizable(False, False)
        self.grab_set()


    def change_text(self, new_text: str=""):
        self.success.configure(text=new_text)


    def build_yesno(self):
        self.buttonFrame = ctk.CTkFrame(master=self)
        self.buttonFrame.configure(fg_color="transparent")
        self.yesBtn = ctk.CTkButton(master=self.buttonFrame, text=self.yes, command=self.yesClick,
                                    font=self.sizes.font4_8, width=self.width // 3)
        self.yesBtn.grid(row=0, column=0, padx=self.sizes.padx)
        self.noBtn = ctk.CTkButton(master=self.buttonFrame, text=self.no, command=self.destroy,
                                   font=self.sizes.font4_8, width=self.width // 3)
        self.noBtn.grid(row=0, column=1, padx=self.sizes.padx)
        self.bind("<Return>", self.yesClick)
        self.buttonFrame.pack()


    def yesClick(self, event=None):
        self.ans = True
        self.destroy()


    def close(self, event=None):
        self.destroy()


    def get_sizes(self):
        return self.sizes


    def close_all(self):
        self.master.close_all()