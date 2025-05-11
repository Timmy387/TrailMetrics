import customtkinter as ctk


class GridDropdown(ctk.CTkFrame):
    def __init__(self, master, og_master,
                 font, dropdown_font,
                 width=None, rows=10, cols=5,
                 values=None, command=None, corner_radius=None):
        super().__init__(master)
        self.og_master = og_master
        self.rows = rows
        self.cols = cols
        self.values = values if values else []
        self.dropdownFont = dropdown_font
        self.command = command
        self.sizes = og_master.get_sizes()
        self.settings = og_master.get_settings()

        self.placed = False
        self.btnWidth = width if width else self.sizes.width // 24
        self.btnHeight = self.sizes.height // 25
        self.dropdownWidth = round(self.btnWidth * self.cols + (self.sizes.padx // 3) * (self.cols * 2))
        self.height = self.btnHeight * self.rows + self.sizes.pady // 3 * (self.rows + 1)
        self.dropDownTextColor = "white"

        self.dropdownBtn = ctk.CTkButton(master=self, text="Select", font=font,
                                            command=self.show_dropdown, corner_radius=corner_radius,
                                         width=self.btnWidth, height=self.btnHeight)
        self.dropdownBtn.pack()

        self.dropdownFrame = None
        self.new_dropdown()


    def set_values(self, values=None):
        if values is not None:
            if self.values == values:
                return
        for child in self.dropdownFrame.winfo_children():
            child.grid_forget()
            child.destroy()
        if values is not None:
            self.values = values
            if len(values) < self.cols:
                self.dropdownWidth = round(self.btnWidth * len(values) + (self.sizes.padx // 3) * (len(values) * 2))
            else:
                self.dropdownWidth = round(self.btnWidth * self.cols + (self.sizes.padx // 3) * (self.cols * 2))
        for i in range(self.rows):
            for j in range(self.cols):
                if i * self.cols + j < len(self.values):
                    value = self.values[i * self.cols + j]
                    btn = ctk.CTkButton(master=self.dropdownFrame, text=value, font=self.dropdownFont,
                                        command=lambda v=value: self.do_command(v),
                                        width=self.btnWidth, height=self.btnHeight, text_color=self.dropDownTextColor,
                                        corner_radius=0, fg_color="transparent")
                    btn.grid(row=i, column=j, padx=self.sizes.padx // 3, pady=self.sizes.pady // 3)


    def do_command(self, value=None):
        self.dropdownBtn.configure(text=value)
        self.show_dropdown()
        if self.command is not None:
            self.command()


    def show_dropdown(self):
        if not self.placed:
            self.set_values()
            winx, winy = self.og_master.current_location()
            sf = self.settings.scale_factor()
            titlebar = round(30 * sf)
            half_dropdown_width = round(self.dropdownWidth // 2)
            x = self.winfo_rootx() // sf - winx + self.btnWidth // 2 - half_dropdown_width - self.sizes.padx
            y = self.winfo_rooty() // sf - winy - titlebar + self.btnHeight + self.sizes.pady // 2
            self.dropdownFrame.place(x=round(x), y=round(y))
            self.dropdownFrame.update_idletasks()
            self.dropdownFrame.lift()
            self.placed = True
        else:
            self.dropdownFrame.place_forget()
            self.dropdownFrame.destroy()
            self.new_dropdown()
            self.placed = False


    def set(self, value):
        self.dropdownBtn.configure(text=value)
        self.dropdownFrame.update_idletasks()


    def get(self):
        return self.dropdownBtn.cget("text")


    def close_dropdown(self):
        if self.placed:
            self.dropdownFrame.place_forget()
            self.dropdownFrame.destroy()
            self.new_dropdown()
            self.placed = False


    def new_dropdown(self):
        self.dropdownFrame = ctk.CTkFrame(master=self.og_master.og_master,
                                          fg_color=("#262626", "#262626"), border_width=2, border_color="grey",
                                          corner_radius=0)


    def dropdown_button_clicked(self, event=None) -> bool:
        for child in self.dropdownBtn.winfo_children():
            if event.widget == child:
                return True
        return False