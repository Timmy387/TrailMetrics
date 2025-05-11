import customtkinter as ctk
from SQLiteFiles.DDL.inserts import delete_trail
from util import split_trail_entry
from GUI.MyCtkObjects.trailSelectFrame import TrailSelectFrame
from GUI.MyCtkObjects.popup import Popup


class DeleteTrail(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.sizes = master.get_sizes()
        self.settings = master.get_settings()
        self.conn = master.get_conn()
        self.transient(master)
        self.grab_set( )
        self.title("Edit Trails")
        self.geometry(f"{self.sizes.new_window_width}x{self.sizes.new_window_height}+"
                      f"{self.sizes.new_window_x}+{self.sizes.new_window_y}")
        self.resizable(False, False)

        self.labelFrame = ctk.CTkFrame(master=self, border_width=2)

        self.editTrailLabel = ctk.CTkLabel(master=self.labelFrame, text="Select a Trail\nto delete",
                                          font=self.sizes.font_full)
        self.editTrailLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx * 2)

        self.labelFrame.pack(pady=self.sizes.pady_title, padx=self.sizes.padx)

        self.trailDropdown = TrailSelectFrame(master=self, og_master=self, label_font=self.sizes.font4_8,
                                              font=self.sizes.font6_8, width=int(self.sizes.width // 2.5),
                                              height=int(self.sizes.height // 16))
        self.trailDropdown.pack(pady=self.sizes.pady * 2)

        self.deleteTrailBtn = ctk.CTkButton(master=self, text="Delete Trail",
                                                command=self.delete_trail,
                                                font=self.sizes.font_full,
                                                width=int(self.sizes.width // 4), height=self.sizes.height // 10)
        self.deleteTrailBtn.pack(pady=self.sizes.pady * 2)

        self.closeBtn = ctk.CTkButton(master=self, text="Close",
                                        command=self.master.close_popup,
                                        font=self.sizes.font_full,
                                        width=int(self.sizes.width // 5), height=self.sizes.height // 12)
        self.closeBtn.pack(pady=self.sizes.pady * 2)

        self.confirmPopup = None
        self.errorMessage = ctk.CTkLabel(master=self, text="", font=self.sizes.font4_8, text_color="red")
        self.successBox = None

        self.bind("<KeyPress>", self.key_press)


    def get_sizes(self):
        return self.sizes

    def get_settings(self):
        return self.settings

    def get_conn(self):
        return self.conn


    def delete_trail(self):
        if self.trailDropdown.get() == "Choose":
            self.errorMessage.configure(text="Please select a trail to delete.")
            self.errorMessage.pack()
            self.after(3000, lambda: self.errorMessage.pack_forget())
            return
        self.confirmPopup = Popup(self, title="Confirm Delete",
                                  text="Are you sure you want\nto delete this trail and\n"
                                       "its associated data?", yesno=True)
        self.wait_window(self.confirmPopup)
        if self.confirmPopup.ans:
            trail_name, county, state = split_trail_entry(self.trailDropdown.get())
            if not delete_trail(self.conn, trail_name, county, state):
                self.errorMessage.configure(text="Deletion failed.")
                self.errorMessage.pack()
                return
            self.trailDropdown.update_trail_list()
            self.trailDropdown.focus_set()
            s = f"Successfully deleted\n{trail_name} in\n{county}, {state}."
            self.successBox = Popup(self, title="Success!", text=s)


    def key_press(self, event=None):
        if event is not None and event.keycode == 27:
            self.master.close_popup()
        elif event is not None and event.keycode == 13:
            self.delete_trail()