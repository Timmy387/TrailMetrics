import customtkinter as ctk
from SQLiteFiles.DatabaseQueries.trails_queries import list_trails


class TrailSelectFrame(ctk.CTkFrame):
    def __init__(self, master, og_master, label_font, font, text="Select from your trails:",
                 side=False, command=None, width=None, height=None, fg_color=None):
        super().__init__(master)
        self.og_master = og_master
        self.sizes = og_master.get_sizes()
        self.conn = og_master.get_conn()
        self.configure(fg_color="transparent")

        if fg_color is not None:
            self.fg_color = fg_color
        else:
            self.fg_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"]

        self.trailLabel = ctk.CTkLabel(master=self, text=text,
                                       font=label_font, text_color=self.fg_color)
        if side:
            self.trailLabel.pack(side="left", anchor="w", padx=self.sizes.padx // 3)
        else:
            self.trailLabel.pack(anchor="w", padx=self.sizes.padx // 3)

        self.fixedSizeFrame = ctk.CTkFrame(master=self, fg_color="transparent",
                width=width if width else self.sizes.width // 4, height=height if height else self.sizes.height // 24)
        self.fixedSizeFrame.pack_propagate(False)
        self.trailDropdown = ctk.CTkOptionMenu(master=self.fixedSizeFrame, dropdown_font=self.sizes.font3_8,
                                               values=list_trails(self.conn), font=font,# fg_color=self.fg_color,
                                               width=width if width else self.sizes.width // 4)
        self.trailDropdown.set("Choose")
        if command:
            self.trailDropdown.configure(command=command)
        self.trailDropdown.pack()
        self.fixedSizeFrame.pack()


    def reset(self):
        self.trailDropdown.set("Choose")
        self.update_trail_list()


    def get(self):
        return self.trailDropdown.get()

    def update_trail_list(self):
        values = list_trails(self.conn)
        if values:
            self.trailDropdown.configure(values=values)
        else:
            self.trailDropdown.configure(values=[])
        self.trailDropdown.set("Choose")