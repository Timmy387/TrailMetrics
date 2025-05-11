import customtkinter as ctk
from GUI.MyCtkObjects.popup import Popup
from GUI.MyCtkObjects.twoLabelSwitch import TwoLabelSwitch


class SettingsPopup(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.sizes = master.get_sizes()
        self.settings = master.get_settings()
        self.grab_set()
        self.transient(master)
        self.title("Settings")
        self.geometry(f"{self.sizes.new_window_width}x{self.sizes.new_window_height}+"
                      f"{self.sizes.new_window_x}+{self.sizes.new_window_y}")
        self.resizable(False, False)

        # choose different setting menus
        self.chooseFrameBar = ctk.CTkFrame(master=self, fg_color="transparent")
        self.chooseFrameBar.columnconfigure((0, 1, 2), weight=1)

        self.graphBtn = ctk.CTkButton(master=self.chooseFrameBar, text="Graph Settings",
                                        command=lambda: self.switch_settings_frame(self.graphSettingsFrame, self.graphBtn),
                                        font=self.sizes.font4_8,
                                        height=self.sizes.height // 24, corner_radius=0)
        self.graphBtn.grid(row=0, column=0, sticky="nsew")

        self.systemBtn = ctk.CTkButton(master=self.chooseFrameBar, text="System Settings",
                                        command=lambda: self.switch_settings_frame(self.systemSettingsFrame, self.systemBtn),
                                        font=self.sizes.font4_8,
                                        height=self.sizes.height // 24, corner_radius=0)
        self.systemBtn.grid(row=0, column=1, sticky="nsew")

        self.otherBtn = ctk.CTkButton(master=self.chooseFrameBar, text="Other Settings",
                                        # command=lambda: self.switch_settings_frame(self.systemSettingsFrame, self.otherBtn),
                                        font=self.sizes.font4_8,
                                        height=self.sizes.height // 24, corner_radius=0)
        self.otherBtn.grid(row=0, column=2, sticky="nsew")

        self.chooseFrameBar.pack(fill="x")



        # whole settings section
        self.settingsSectionFrame = ctk.CTkFrame(master=self,
                                                 width=int(self.sizes.new_window_width * 0.9),
                                                 height=int(self.sizes.new_window_height * 0.6))
        # self.settingsSectionFrame.pack_propagate(False)

        # graph settings
        self.graphSettingsFrame = ctk.CTkFrame(master=self.settingsSectionFrame, fg_color="transparent")

        # switches for graph context
        self.switchesFrame = ctk.CTkFrame(master=self.graphSettingsFrame, fg_color="transparent")

        self.totalOrAvgSwitch = TwoLabelSwitch(master=self.switchesFrame, left="Total", right="Average",
                                               sizes=self.sizes)
        if self.settings.total_or_avg() == 1:
            self.totalOrAvgSwitch.select()
        self.totalOrAvgSwitch.grid(row=0, column=0, pady=self.sizes.pady * 3, padx=self.sizes.padx * 3)

        self.cmpTrailOrDateSwitch = TwoLabelSwitch(master=self.switchesFrame, left="Compare\nTrails",
                                                   right="Compare\nDates",
                                                   sizes=self.sizes)
        if self.settings.cmp_trails_or_dates() == 1:
            self.cmpTrailOrDateSwitch.select()
        self.cmpTrailOrDateSwitch.grid(row=1, column=0, pady=self.sizes.pady * 3, padx=self.sizes.padx * 3)

        self.legendSwitch = ctk.CTkSwitch(master=self.switchesFrame, text="Show legend", font=self.sizes.font3_8)
        if self.settings.legend() == 1:
            self.legendSwitch.select()
        self.legendSwitch.grid(row=2, column=0, pady=self.sizes.pady * 3, padx=self.sizes.padx * 3)

        self.gridSwitch = ctk.CTkSwitch(master=self.switchesFrame, text="Show grid", font=self.sizes.font3_8)
        if self.settings.grid() == 1:
            self.gridSwitch.select()
        self.gridSwitch.grid(row=0, column=1, pady=self.sizes.pady * 3, padx=self.sizes.padx * 3)

        self.graphTypeDropdown = ctk.CTkOptionMenu(master=self.switchesFrame,
                                                   values=["Line", "Bar", "Scatter"],
                                                   font=self.sizes.font3_8)
        self.graphTypeDropdown.set(self.settings.graph_type().title())
        self.graphTypeDropdown.grid(row=1, column=1, pady=self.sizes.pady * 3, padx=self.sizes.padx * 3)

        self.zoomSwitch = TwoLabelSwitch(master=self.switchesFrame, left="Zoom\nout", right="Zoom\nin",
                                         sizes=self.sizes)
        self.zoomSwitch = ctk.CTkSwitch(master=self.switchesFrame, text="Always\nstart Y-axis\nat zero",
                                        font=self.sizes.font3_8)
        if self.settings.zoom_graph():
            self.zoomSwitch.select()
        self.zoomSwitch.grid(row=2, column=1, pady=self.sizes.pady * 3, padx=self.sizes.padx * 3)

        self.switchesFrame.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.currentFrame = self.graphSettingsFrame
        self.currentBtn = self.graphBtn
        self.switch_settings_frame(self.graphSettingsFrame, self.graphBtn)

        self.settingsSectionFrame.pack(pady=self.sizes.pady * 3, padx=self.sizes.padx * 2, fill="both", expand=True)



        # system settings
        self.systemSettingsFrame = ctk.CTkFrame(master=self.settingsSectionFrame, fg_color="transparent")

        # Theme
        self.themeFrame = ctk.CTkFrame(master=self.systemSettingsFrame)

        self.themeLabel = ctk.CTkLabel(master=self.themeFrame, text="Theme", font=self.sizes.font4_8)
        self.themeLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.themeDropdown = ctk.CTkOptionMenu(master=self.themeFrame,
                                                values=["Light", "Dark"], # TODO no system theme for now
                                                font=self.sizes.font4_8)
        self.themeInit = self.settings.theme()
        self.themeDropdown.set(self.themeInit)
        self.themeDropdown.pack()

        self.themeFrame.grid(row=0, column=0, padx=self.sizes.padx, pady=self.sizes.pady)

        # Color Scheme
        self.colorSchemeFrame = ctk.CTkFrame(master=self.systemSettingsFrame)

        self.colorSchemeLabel = ctk.CTkLabel(master=self.colorSchemeFrame, text="Color Scheme", font=self.sizes.font4_8)
        self.colorSchemeLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.colorSchemeDropdown = ctk.CTkOptionMenu(master=self.colorSchemeFrame,
                                                     values=["Blue", "Green", "Dark Blue"],
                                                     font=self.sizes.font4_8)
        color = self.settings.color_scheme().replace("-", " ").title()
        self.colorInit = color
        self.colorSchemeDropdown.set(color)
        self.colorSchemeDropdown.pack()

        self.colorSchemeFrame.grid(row=0, column=1, padx=self.sizes.padx, pady=self.sizes.pady)

        # Scale
        self.scaleFrame = ctk.CTkFrame(master=self.systemSettingsFrame)

        self.scaleLabel = ctk.CTkLabel(master=self.scaleFrame, text="Scale", font=self.sizes.font4_8)
        self.scaleLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.scaleInit = int(self.settings.window_scale() * 10 + 1)
        self.scaleSlider = ctk.CTkSlider(master=self.scaleFrame, from_=6, to=10, number_of_steps=4)
        self.scaleSlider.set(self.scaleInit)
        self.scaleSlider.pack()

        self.scaleFrame.grid(row=1, column=0, padx=self.sizes.padx, pady=self.sizes.pady)

        # font
        self.fontFrame = ctk.CTkFrame(master=self.systemSettingsFrame)
        self.fontLabel = ctk.CTkLabel(master=self.fontFrame, text="Font", font=self.sizes.font4_8)
        self.fontLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.fontDropdown = ctk.CTkOptionMenu(master=self.fontFrame,
                                              values=["Arial", "Courier", "Roboto",
                                                      "Helvetica"],
                                              font=self.sizes.font4_8)
        self.fontInit = self.settings.font()
        self.fontDropdown.set(self.fontInit)
        self.fontDropdown.pack()

        self.fontFrame.grid(row=1, column=1, padx=self.sizes.padx, pady=self.sizes.pady)


        self.buttonFrame = ctk.CTkFrame(master=self)
        self.applyBtn = ctk.CTkButton(master=self.buttonFrame, text="Apply changes",
                                      command=self.apply_changes, font=self.sizes.font7_8,
                                      width=int(self.sizes.width // 4.5), height=self.sizes.height // 16)
        self.applyBtn.grid(row=0, column=0, padx=self.sizes.padx, pady=self.sizes.pady)

        self.defaultsBtn = ctk.CTkButton(master=self.buttonFrame, text="Reset to defaults",
                                         command=self.back_to_defaults, font=self.sizes.font7_8,
                                         width=int(self.sizes.width // 4.5), height=self.sizes.height // 16)
        self.defaultsBtn.grid(row=0, column=1, padx=self.sizes.padx, pady=self.sizes.pady)

        self.cancelBtn = ctk.CTkButton(master=self.buttonFrame, text="Close",
                                       command=self.destroy, font=self.sizes.font5_8,
                                       width=self.sizes.width // 6, height=self.sizes.height // 16)
        self.cancelBtn.grid(row=1, column=0, columnspan=2, pady=self.sizes.pady)
        self.buttonFrame.pack(side="bottom", pady=self.sizes.pady_title, padx=self.sizes.padx)


        self.bind("<KeyPress>", self.key_press)



    def change_theme(self, theme):
        self.settings.update_config("settings", "theme", theme)
        ctk.set_appearance_mode(theme)
        # self.update()


    def change_color_scheme(self, color_scheme):
        color_scheme = color_scheme.replace(" ", "-").lower()
        self.settings.update_config("settings", "colorScheme", color_scheme)


    def apply_changes(self, btnPressed=None):
        self.settings.update_config("settings", "graphSettings", {
            "totalOrAvg": self.totalOrAvgSwitch.get(),
            "cmpTrailsOrDates": self.cmpTrailOrDateSwitch.get(),
            "legend": True if self.legendSwitch.get() else False,
            "grid": True if self.gridSwitch.get() else False,
            "graphType": self.graphTypeDropdown.get(),
            "zoomGraph": True if self.zoomSwitch.get() else False
        })

        self.master.build_graph_info()
        # self.master.build_graphs(popup=False)

        if self.fontDropdown.get() != self.fontInit\
                or self.scaleSlider.get() != self.scaleInit\
                or self.colorSchemeDropdown.get() != self.colorInit\
                or self.themeDropdown.get() != self.themeInit:
            if not self.reloadPopup():
                self.fontDropdown.set(self.fontInit)
                self.scaleSlider.set(self.scaleInit)
                self.colorSchemeDropdown.set(self.colorInit)
                self.themeDropdown.set(self.themeInit)
                return
            if self.scaleSlider.get() != self.scaleInit:
                self.settings.update_config("settings", "useScale", True)
            self.settings.update_config("settings", "theme", self.themeDropdown.get())
            self.settings.update_config("settings", "font", self.fontDropdown.get())
            self.settings.update_config("settings", "windowScale", (self.scaleSlider.get() - 1) / 10)
            self.settings.update_config("settings", "colorScheme",
                                        self.colorSchemeDropdown.get().replace(" ", "-").lower())
            self.close_all(True)


    def back_to_defaults(self):
        defaults = self.settings.get_defaults()
        self.fontDropdown.set(defaults["font"])
        self.scaleSlider.set(int(defaults["windowScale"] * 10 + 1))
        self.colorSchemeDropdown.set(defaults["colorScheme"].replace("-", " ").title())
        self.themeDropdown.set(defaults["theme"])
        self.totalOrAvgSwitch.select()
        self.cmpTrailOrDateSwitch.select()
        self.legendSwitch.select()
        self.gridSwitch.deselect()
        self.graphTypeDropdown.set(defaults["graphSettings"]["graphType"].title())
        self.zoomSwitch.select()


    def key_press(self, event=None):
        if event is not None and event.keycode == 13 and event.state != 1: # enter
            self.apply_changes()
        elif event is not None and event.keycode == 27: # esc
            self.master.close_popup()


    def close_all(self, reopen=False):
        self.master.close_all(reopen)


    def reloadPopup(self):
        rp = Popup(master=self, title="Restart Required",
                   text="Please close and restart\nthe app for your changes\nto take effect.",
                   yesno=True, yes="Restart", no="Cancel", width=self.sizes.width // 3)
        self.wait_window(rp)
        return rp.ans


    def get_settings(self):
        return self.settings


    def get_sizes(self):
        return self.sizes


    def switch_settings_frame(self, new_frame, btn=None):
        self.currentFrame.pack_forget()
        default_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        self.currentBtn.configure(fg_color=default_color, text_color="white")
        btn.configure(fg_color="grey", text_color="black")
        new_frame.pack(pady=self.sizes.pady * 2)
        self.currentFrame = new_frame
        self.currentBtn = btn


    def get_graph_settings(self):
        return {
            "totalOrAvg": self.totalOrAvgSwitch.get(),
            "cmpTrailsOrDates": self.cmpTrailOrDateSwitch.get(),
            "legend": self.legendSwitch.get(),
            "grid": self.gridSwitch.get(),
            "graphType": self.graphTypeDropdown.get(),
            "zoomGraph": self.zoomSwitch.get()
        }