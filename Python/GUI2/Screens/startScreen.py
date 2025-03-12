import customtkinter as ctk
from GUI2.Screens.addTrailPopup import AddTrail
from GUI2.Screens.importDataPopup import ImportData
from GUI2.Screens.settingsPopup import SettingsPopup


class StartScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.sizes = master.get_sizes()
        self.settings = master.get_settings()
        self.title = ctk.CTkLabel(master=self, text="Choose what data you want to view!", font=self.sizes.font_full)
        self.title.pack(pady=self.sizes.pady_title)

        self.otherBtns = ctk.CTkFrame(master=self)
        self.btnWidth = self.sizes.width // 10
        self.btnHeight = self.sizes.height // 12

        self.uploadFileBtn = ctk.CTkButton(master=self.otherBtns, text="Upload a\nfile",
                                           command=lambda: self.open_popup(ImportData), font=self.sizes.font4_8,
                                           width=self.btnWidth, height=self.btnHeight)
        self.uploadFileBtn.grid(row=0, column=0, padx=self.sizes.padx, pady=self.sizes.pady)

        self.addTrailBtn = ctk.CTkButton(master=self.otherBtns, text="Edit\ntrails",
                                         command=lambda: self.open_popup(AddTrail), font=self.sizes.font4_8,
                                         width=self.btnWidth, height=self.btnHeight)

        self.addTrailBtn.grid(row=0, column=1, padx=self.sizes.padx, pady=self.sizes.pady)

        self.saveGraphBtn = ctk.CTkButton(master=self.otherBtns, text="Save\ngraph",
                                         command=self.save_graph, font=self.sizes.font4_8,
                                         width=self.btnWidth, height=self.btnHeight)
        self.saveGraphBtn.grid(row=0, column=2, padx=self.sizes.padx, pady=self.sizes.pady)

        self.settingsBtn = ctk.CTkButton(master=self.otherBtns, text="Settings",
                                         command=lambda: self.open_popup(SettingsPopup), font=self.sizes.font4_8,
                                         width=self.btnWidth, height=self.btnHeight)
        self.settingsBtn.grid(row=0, column=3, padx=self.sizes.padx, pady=self.sizes.pady)

        self.quitBtn = ctk.CTkButton(master=self.otherBtns, text="Quit", font=self.sizes.font4_8,
                                     command=self.master.close_all,
                                     width=self.btnWidth, height=self.btnHeight)
        self.quitBtn.grid(row=0, column=4, padx=self.sizes.padx, pady=self.sizes.pady)

        self.popup = None
        self.otherBtns.pack(side="bottom", anchor="se", padx=self.sizes.padx * 2, pady=self.sizes.pady * 2)


    def open_popup(self, popup_class):
        self.popup = popup_class(self)


    def close_popup(self):
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None
        # self.popup.withdraw()
        # self.grab_set()


    def close_all(self):
        self.master.close_all()


    def get_settings(self):
        return self.settings


    def get_sizes(self):
        return self.sizes


    def refresh_scheme(self):
        self.master.refresh_scheme()


    def save_graph(self):
        pass