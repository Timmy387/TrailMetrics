import customtkinter as ctk

class TwoLabelButton(ctk.CTkFrame):
    def __init__(self, master, og_master,
                 text_left, text_right, font,
                 width, height,
                 command, font_color=None,
                 corner_radius=None):
        super().__init__(master, fg_color="transparent", corner_radius=corner_radius,
                         width=width)
        self.og_master = og_master
        self.sizes = og_master.get_sizes()
        self.height = font[1] * 3 - self.sizes.pady * 2
        self.configure(height=self.height + self.sizes.pady)
        self.font = font
        self.pack_propagate(False)
        self.command = command
        self.default_color = "transparent"
        self.hover_color = "#505050"

        self.label_left = ctk.CTkLabel(self, text=text_left, anchor="w", font=self.font, corner_radius=corner_radius,
                                       fg_color="transparent", height=self.height, text_color=font_color)
        self.label_right = ctk.CTkLabel(self, text=text_right, anchor="e", font=self.font, corner_radius=corner_radius,
                                        fg_color="transparent", height=self.height, text_color="gray")

        self.label_left.pack(side="left", expand=True, fill="x", padx=self.sizes.padx // 2)
        self.label_right.pack(side="right", padx=self.sizes.padx // 2)

        # Make the whole frame clickable
        self.bind_events(self)
        self.bind_events(self.label_left)
        self.bind_events(self.label_right)

    def bind_events(self, widget):
        widget.bind("<Enter>", lambda e: self.configure(fg_color=self.hover_color))
        widget.bind("<Leave>", lambda e: self.configure(fg_color=self.default_color))
        widget.bind("<Button-1>", self.on_click)
        widget.configure(cursor="hand2")

    def on_click(self, event):
        self.command()