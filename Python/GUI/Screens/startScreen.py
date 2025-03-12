import customtkinter as ctk
from GUI.Screens.addTrailScreen import AddTrail
from GUI.Screens.importDataScreen import ImportData
from GUI.Screens.viewDataScreen import ViewData


class StartScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title = ctk.CTkLabel(master=self, text="Hey Pete! What would you\nlike to work on today?", font=("Roboto", 40))
        self.title.pack(pady=40)
        self.addTrailBtn = ctk.CTkButton(master=self, text="Add a trail", command=self.trail_add,
                                         width=300, height=80, font=("Roboto", 30))
        self.addTrailBtn.pack(pady=15)
        self.importDataBtn = ctk.CTkButton(master=self, text="Import trail data", command=self.data_add,
                                           width=300, height=80, font=("Roboto", 30))
        self.importDataBtn.pack(pady=15)
        self.viewDataBtn = ctk.CTkButton(master=self, text="View trail data", command=self.data_view,
                                         width=300, height=80, font=("Roboto", 30))
        self.viewDataBtn.pack(pady=15)

    def trail_add(self):
        self.master.switch_frame(AddTrail)

    def data_add(self):
        self.master.switch_frame(ImportData)

    def data_view(self):
        self.master.switch_frame(ViewData)