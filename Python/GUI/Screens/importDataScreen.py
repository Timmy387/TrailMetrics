import customtkinter as ctk


class ImportData(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.returnBtn = ctk.CTkButton(master=self, text="Return to\nmain menu", command=self.master.rtn,
                                         width=60, height=20, font=("Roboto", 20))
        self.returnBtn.place(relx=1.0, rely=1.0, anchor=ctk.SE, x=-20, y=-20)