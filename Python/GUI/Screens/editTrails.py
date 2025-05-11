import customtkinter as ctk
from GUI.Screens.addTrailPopup import AddTrail
from GUI.Screens.deleteTrailPopup import DeleteTrail

class EditTrails(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.sizes = master.get_sizes()
        self.settings = master.get_settings()
        self.conn = master.get_conn()
        self.transient(master)
        self.grab_set()
        self.title("Edit Trails")
        self.geometry(f"{self.sizes.new_window_width - 50}x{self.sizes.new_window_height - 50}+"
                      f"{self.sizes.new_window_x - 25}+{self.sizes.new_window_y - 25}")
        self.resizable(False, False)

        self.labelFrame = ctk.CTkFrame(master=self, border_width=2)

        self.editTrailLabel = ctk.CTkLabel(master=self.labelFrame, text="Add or delete\na trail",
                                          font=self.sizes.font_full)
        self.editTrailLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx * 2)

        self.labelFrame.pack(pady=self.sizes.pady_title, padx=self.sizes.padx)

        self.popup = None

        self.addTrailBtn = ctk.CTkButton(master=self, text="Add Trail",
                                          width=int(self.sizes.width // 4), height=self.sizes.height // 10,
                                          font=self.sizes.font_full, command=lambda: self.open_popup(AddTrail))

        self.addTrailBtn.pack(pady=self.sizes.pady * 2)

        self.deleteTrailBtn = ctk.CTkButton(master=self, text="Delete Trail",
                                                width=int(self.sizes.width // 4), height=self.sizes.height // 10,
                                                font=self.sizes.font_full, command=lambda: self.open_popup(DeleteTrail))
        self.deleteTrailBtn.pack(pady=self.sizes.pady * 2)

        self.closeBtn = ctk.CTkButton(master=self, text="Close",
                                      width=int(self.sizes.width // 5), height=self.sizes.height // 12,
                                        font=self.sizes.font_full, command=self.master.close_popup)
        self.closeBtn.pack(pady=self.sizes.pady * 2)

        self.bind("<KeyPress>", func=self.key_press)


    def open_popup(self, popup_class):
        self.popup = popup_class(self)


    def close_popup(self):
        if self.popup is not None:
            self.master.build_graph_info()
            self.popup.destroy()
            self.popup = None

    def get_sizes(self):
        return self.sizes

    def get_settings(self):
        return self.settings

    def get_conn(self):
        return self.conn


    def key_press(self, event):
        if event.keysym == "Escape":
            self.master.close_popup()