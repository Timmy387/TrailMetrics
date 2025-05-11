import customtkinter as ctk


class TwoLabelSwitch(ctk.CTkFrame):
    def __init__(self, master, left, right, sizes, command=None):
        super().__init__(master)
        self.left = left
        self.right = right
        self.command = command
        self.sizes = sizes
        self.configure(fg_color="transparent")
        self.columnconfigure((0, 1), weight=1)

        self.leftLabel = ctk.CTkLabel(master=self, text=self.left, font=self.sizes.font3_8)
        self.leftLabel.grid(row=0, column=0)
        # justify text to right
        self.leftLabel.configure(justify="right")

        self.switch = ctk.CTkSwitch(master=self, text=self.right, font=self.sizes.font3_8)
        if self.command is not None:
            self.switch.configure(command=self.command)
        self.switch.grid(row=0, column=1, padx=self.sizes.padx)


    def select(self):
        self.switch.select(1)


    def deselect(self):
        self.switch.deselect(1)


    def get(self):
        return self.switch.get()


    def enable(self):
        self.switch.configure(state="normal")
        text_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"]
        self.leftLabel.configure(text_color=text_color)


    def disable(self):
        self.switch.configure(state="disabled")
        self.leftLabel.configure(text_color="grey")