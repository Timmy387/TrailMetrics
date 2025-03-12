import customtkinter as ctk
from GUI2.popup import Popup


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

        self.labelFrame = ctk.CTkFrame(master=self, border_width=2)

        self.uploadFileLabel = ctk.CTkLabel(master=self.labelFrame, text="Settings",
                                          font=self.sizes.font_full)
        self.uploadFileLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.labelFrame.pack(pady=self.sizes.pady_title, padx=self.sizes.padx)

        self.settingsGrid = ctk.CTkFrame(master=self)

        # Theme
        self.themeFrame = ctk.CTkFrame(master=self.settingsGrid)

        self.themeLabel = ctk.CTkLabel(master=self.themeFrame, text="Theme", font=self.sizes.font4_8)
        self.themeLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.themeDropdown = ctk.CTkOptionMenu(master=self.themeFrame,
                                                values=["Light", "Dark", "System"],
                                                font=self.sizes.font4_8)
        self.themeInit = self.settings.theme
        self.themeDropdown.set(self.themeInit)
        self.themeDropdown.pack()

        self.themeFrame.grid(row=0, column=0, padx=self.sizes.padx, pady=self.sizes.pady)

        # Color Scheme
        self.colorSchemeFrame = ctk.CTkFrame(master=self.settingsGrid)

        self.colorSchemeLabel = ctk.CTkLabel(master=self.colorSchemeFrame, text="Color Scheme", font=self.sizes.font4_8)
        self.colorSchemeLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.colorSchemeDropdown = ctk.CTkOptionMenu(master=self.colorSchemeFrame,
                                                     values=["Blue", "Green", "Dark Blue"],
                                                     font=self.sizes.font4_8)
        color = self.settings.colorScheme.replace("-", " ").title()
        self.colorInit = color
        self.colorSchemeDropdown.set(color)
        self.colorSchemeDropdown.pack()

        self.colorSchemeFrame.grid(row=0, column=1, padx=self.sizes.padx, pady=self.sizes.pady)

        # Scale
        self.scaleFrame = ctk.CTkFrame(master=self.settingsGrid)

        self.scaleLabel = ctk.CTkLabel(master=self.scaleFrame, text="Scale", font=self.sizes.font4_8)
        self.scaleLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.scaleInit = int(self.settings.windowScale * 10 + 1)
        self.scaleSlider = ctk.CTkSlider(master=self.scaleFrame, from_=6, to=10, number_of_steps=4)
        self.scaleSlider.set(self.scaleInit)
        self.scaleSlider.pack()

        self.scaleFrame.grid(row=1, column=0, padx=self.sizes.padx, pady=self.sizes.pady)

        # font
        self.fontFrame = ctk.CTkFrame(master=self.settingsGrid)
        self.fontLabel = ctk.CTkLabel(master=self.fontFrame, text="Font", font=self.sizes.font4_8)
        self.fontLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.fontDropdown = ctk.CTkOptionMenu(master=self.fontFrame,
                                              values=["Arial", "Courier", "Roboto",
                                                      "Helvetica"],
                                              font=self.sizes.font4_8)
        self.fontInit = self.settings.font
        self.fontDropdown.set(self.fontInit)
        self.fontDropdown.pack()

        self.fontFrame.grid(row=1, column=1, padx=self.sizes.padx, pady=self.sizes.pady)

        self.settingsGrid.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.applyFrame = ctk.CTkFrame(master=self)
        self.applyBtn = ctk.CTkButton(master=self.applyFrame, text="Apply changes",
                                      command=self.apply_changes, font=self.sizes.font7_8,
                                      width=int(self.sizes.width // 4.5), height=self.sizes.height // 16)
        self.applyBtn.grid(row=0, column=0, padx=self.sizes.padx, pady=self.sizes.pady)

        self.defaultsBtn = ctk.CTkButton(master=self.applyFrame, text="Reset to defaults",
                                         command=self.back_to_defaults, font=self.sizes.font7_8,
                                         width=int(self.sizes.width // 4.5), height=self.sizes.height // 16)
        self.defaultsBtn.grid(row=0, column=1, padx=self.sizes.padx, pady=self.sizes.pady)

        self.cancelBtn = ctk.CTkButton(master=self.applyFrame, text="Cancel",
                                        command=self.destroy, font=self.sizes.font5_8,
                                        width=self.sizes.width // 6, height=self.sizes.height // 16)
        self.cancelBtn.grid(row=1, column=0, columnspan=2, pady=self.sizes.pady)

        self.applyFrame.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.bind("<KeyPress>", self.key_press)



    def change_theme(self, theme):
        self.settings.update_config("settings", "theme", theme)
        ctk.set_appearance_mode(theme)
        # self.update()


    def change_color_scheme(self, color_scheme):
        color_scheme = color_scheme.replace(" ", "-").lower()
        self.settings.update_config("settings", "colorScheme", color_scheme)


    def apply_changes(self, btnPressed=None):
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
            self.settings.update_config("settings", "theme", self.themeDropdown.get())
            self.settings.update_config("settings", "font", self.fontDropdown.get())
            self.settings.update_config("settings", "useScale", True)
            self.settings.update_config("settings", "windowScale", (self.scaleSlider.get() - 1) / 10)
            self.settings.update_config("settings", "colorScheme",
                                        self.colorSchemeDropdown.get().replace(" ", "-").lower())
            self.close_all()


    def back_to_defaults(self):
        defaults = self.settings.get_defaults()
        self.fontDropdown.set(defaults["font"])
        self.scaleSlider.set(int(defaults["windowScale"] * 10 + 1))
        self.colorSchemeDropdown.set(defaults["colorScheme"].replace("-", " ").title())
        self.themeDropdown.set(defaults["theme"])


    def key_press(self, event=None):
        if event is not None and event.keycode == 13 and event.state != 1: # enter
            self.apply_changes()
        elif event is not None and event.keycode == 27: # esc
            self.master.close_popup()


    def close_all(self):
        self.master.close_all()


    def reloadPopup(self):
        rp = Popup(master=self, title="Restart Required",
                   text="Please close and restart\nthe app for your changes\nto take effect.",
                   yesno=True, yes="Restart", no="Cancel", width=self.sizes.width // 3, height=int(self.sizes.height // 4))
        self.wait_window(rp)
        return rp.ans


    def get_settings(self):
        return self.settings


    def get_sizes(self):
        return self.sizes