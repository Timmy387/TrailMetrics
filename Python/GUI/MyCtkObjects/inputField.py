import customtkinter as ctk

class InputField(ctk.CTkFrame):
    def __init__(self, master, label_text, placeholder_text=None, button: tuple=None, validate=None, validatecommand=None):
        super().__init__(master)
        self.sizes = master.get_sizes()
        self.configure(fg_color="transparent")

        self.label = ctk.CTkLabel(master=self, text=label_text, font=self.sizes.font4_8)

        self.input = None
        self.button = None
        self.textButtonFrame = None

        if button:
            self.build_inline_button(placeholder_text, button, validate, validatecommand)
        else:
            self.label.pack(anchor="w", padx=self.sizes.padx // 2)
            self.input = ctk.CTkEntry(master=self, font=self.sizes.font7_8, placeholder_text=placeholder_text,
                                    width=int(self.sizes.new_window_width * 0.6),
                                    validate=validate, validatecommand=validatecommand)
            self.input.pack()


    def get(self):
        return self.input.get()


    def focus_set(self):
        self.input.focus_set()


    def insert(self, text):
        self.input.delete(0, ctk.END)
        self.input.insert(0, text)


    def build_inline_button(self, placeholder_text, button, validate, validatecommand):
        self.label.pack(anchor="w", padx=self.sizes.padx)
        self.textButtonFrame = ctk.CTkFrame(master=self, fg_color="transparent")

        self.input = ctk.CTkEntry(master=self.textButtonFrame, font=self.sizes.font5_8,
                                placeholder_text=placeholder_text, width=int(self.sizes.new_window_width * 0.7),
                                validate=validate, validatecommand=validatecommand)
        self.input.grid(row=0, column=0, padx=self.sizes.padx // 3, pady=0)

        self.button = ctk.CTkButton(master=self.textButtonFrame, text=button[0],
                                    font=self.sizes.font5_8, command=button[1],
                                    width=int(self.sizes.new_window_width * 0.15))
        self.button.grid(row=0, column=1, pady=0)

        self.textButtonFrame.pack()


    def get_sizes(self):
        return self.sizes
