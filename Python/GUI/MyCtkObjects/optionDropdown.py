import customtkinter as ctk
from GUI.MyCtkObjects.twoLabelButton import TwoLabelButton

class OptionDropdown(ctk.CTkFrame):
    def __init__(self, master, og_master, label, font,
                 width, dropdown_width, dropdown_font,
                 values, commands, shortcuts=None, corner_radius=None):
        super().__init__(master=master, fg_color="transparent")
        self.og_master = og_master
        self.label = label
        self.font = font
        self.width = width
        self.dropdownWidth = dropdown_width
        self.dropdownFont = dropdown_font
        self.values = values
        self.commands = commands
        self.corner_radius = corner_radius
        self.sizes = og_master.get_sizes()
        self.settings = og_master.get_settings()
        self.fontColor = "white"
        self.shortcuts = shortcuts if shortcuts is not None else [""] * len(values)

        self.placed = False
        self.btnHeight = self.sizes.height // 25

        self.dropdownBtn = ctk.CTkButton(master=self, text=self.label, font=self.font,
                                         command=self.show_dropdown, corner_radius=self.corner_radius,
                                         height=self.btnHeight, width=self.width)

        self.dropdownBtn.pack()
        self.dropdownFrame = None
        self.new_dropdown()

        self.lastClicked = ""


    def set_values(self, values=None):
        if values is not None:
            if self.values == values:
                return
            self.values = values
        for child in self.dropdownFrame.winfo_children():
            child.grid_forget()
            child.destroy()
        for i, value in enumerate(self.values):
            btn = TwoLabelButton(master=self.dropdownFrame, og_master=self,
                                 text_left=value, text_right=self.shortcuts[i],
                                 width=self.dropdownWidth, height=self.btnHeight,
                                 command=self.commands[i], font=self.dropdownFont,
                                 corner_radius=self.corner_radius, font_color=self.fontColor)
            btn.pack(anchor="w", padx=self.sizes.padx // 2, pady=self.sizes.pady // 2)

    def do_command(self, value):
        self.lastClicked = value
        return value

    def new_dropdown(self):
        self.dropdownFrame = ctk.CTkFrame(master=self.og_master,
                                          fg_color=("#262626", "#262626"), border_width=1, border_color="grey",
                                          corner_radius=0)


    def show_dropdown(self):
        if self.placed:
            self.dropdownFrame.place_forget()
            self.dropdownFrame.destroy()
            self.new_dropdown()
            self.placed = False
        else:
            # place dropdown frame so left edge aligns with the dropdownBtn
            self.placed = True
            self.set_values()
            sf = self.settings.scale_factor()
            titlebar = round(30 * sf)
            winx, winy = self.og_master.current_location()
            x = self.winfo_x() + self.sizes.padx // 2
            y = self.winfo_rooty() // sf - winy - titlebar + self.btnHeight + self.sizes.pady * 2
            self.dropdownFrame.place(x=x, y=y)
            self.dropdownFrame.update_idletasks()
            self.dropdownFrame.lift()

    def close_dropdown(self):
        if self.placed:
            self.dropdownFrame.place_forget()
            self.dropdownFrame.destroy()
            self.new_dropdown()
            self.placed = False


    def dropdown_btn_clicked(self, event=None) -> bool:
        for child in self.dropdownBtn.winfo_children():
            if event.widget == child:
                return True
        return False


    def get_sizes(self):
        return self.sizes
