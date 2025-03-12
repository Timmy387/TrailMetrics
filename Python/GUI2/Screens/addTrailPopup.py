import customtkinter as ctk

from SQLiteFiles.DatabaseQueries.trails_queries import is_trail
from connect_sqlite import connect_trail_db_sqlite
from SQLiteFiles.DDL.inserts import insert_trail, delete_trail
from SQLiteFiles.DatabaseQueries.trail_location_queries import is_state, is_county_in_state
from GUI2.popup import Popup
from GUI2.inputField import InputField


class AddTrail(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        def on_validate_input(P):
            # P = P.upper()
            # Allow only up to 2 characters
            if len(P) <= 2:
                return True
            return False

        self.sizes = master.get_sizes()
        self.settings = master.get_settings()
        self.transient(master)
        self.grab_set()
        self.title("Edit Trails")
        self.geometry(f"{self.sizes.new_window_width}x{self.sizes.new_window_height}+"
                      f"{self.sizes.new_window_x}+{self.sizes.new_window_y}")
        self.resizable(False, False)

        self.labelFrame = ctk.CTkFrame(master=self, border_width=2)

        self.addTrailLabel = ctk.CTkLabel(master=self.labelFrame, text="Add or delete a trail by\nfilling in the info below!",
                                          font=self.sizes.font_full)
        self.addTrailLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx * 2)

        self.labelFrame.pack(pady=self.sizes.pady * 2, padx=self.sizes.padx)

        self.trailNameInput = InputField(master=self, label_text="Trail name:", placeholder_text="Trail name")
        self.trailNameInput.pack(pady=self.sizes.pady)
        self.after(50, self.trailNameInput.focus_set)

        self.countyInput = InputField(master=self, label_text="County:", placeholder_text="County")
        self.countyInput.pack(pady=self.sizes.pady)

        vcmd = (self.register(on_validate_input), "%P")
        self.stateInput = InputField(master=self, label_text="State:", placeholder_text="St", validate="key",
                                     validatecommand=vcmd)
        self.stateInput.pack(pady=self.sizes.pady)

        self.buttonFrame = ctk.CTkFrame(master=self)

        self.enterTrailBtn = ctk.CTkButton(master=self.buttonFrame, text="Enter new trail!",
                                           width=int(self.sizes.width // 4.5), height=self.sizes.height // 16,
                                           font=self.sizes.font7_8, command=self.validate_trail_input)
        self.enterTrailBtn.grid(row=0, column=0, padx=self.sizes.padx, pady=self.sizes.pady)

        self.deleteTrailBtn = ctk.CTkButton(master=self.buttonFrame, text="Delete old trail!",
                                            width=int(self.sizes.width // 4.5), height=self.sizes.height // 16,
                                            font=self.sizes.font7_8, command=lambda: self.validate_trail_input(True))
        self.deleteTrailBtn.grid(row=0, column=1, padx=self.sizes.padx, pady=self.sizes.pady)

        self.cancelBtn = ctk.CTkButton(master=self.buttonFrame, text="Cancel",
                                        width=self.sizes.width // 6, height=self.sizes.height // 16,
                                        font=self.sizes.font5_8,
                                        command=self.master.close_popup)
        self.cancelBtn.grid(row=1, column=0, columnspan=2, pady=self.sizes.pady)

        self.buttonFrame.pack(pady=self.sizes.pady)

        self.errorMessage = ctk.CTkLabel(master=self, font=self.sizes.font4_8,text_color="red")

        self.confirmPopup = None
        self.successBox = None

        self.bind("<KeyPress>", func=self.key_press)



    def validate_trail_input(self, deleting=False) -> bool:
        conn = connect_trail_db_sqlite()
        self.errorMessage.pack_forget()
        trail_name = self.trailNameInput.get()
        state = self.stateInput.get()
        county = self.format_county(self.countyInput.get())
        if deleting and len(trail_name) == 0:
            self.errorMessage.configure(text="Please enter a trail name to delete!")
            self.errorMessage.pack()
            conn.close()
            return False

        elif not deleting and (len(trail_name) == 0 or len(county) == 0 or len(state) == 0):
            self.errorMessage.configure(text="Please fill in all fields!")
            self.errorMessage.pack()
            conn.close()
            return False

        elif not deleting and not is_state(conn, state):
            self.errorMessage.configure(text=f"{self.stateInput.get().upper()} is not a US state!")
            self.errorMessage.pack()
            conn.close()
            return False

        elif not deleting and not is_county_in_state(conn, county, state):
            self.errorMessage.configure(text=f"{county} is not a county in {state.upper()}!")
            self.errorMessage.pack()
            conn.close()
            return False

        if deleting:
            if not is_trail(conn, trail_name):
                self.errorMessage.configure(text="Trail does not exist in database!")
                self.errorMessage.pack()
                conn.close()
                return False
            elif is_trail(conn, trail_name):
                self.confirmPopup = Popup(self, title="Confirm Delete",
                                          text="Are you sure you want\nto delete this trail and\n"
                                               "its associated data?",
                                          width=self.sizes.width // 3, height=self.sizes.height // 4, yesno=True)
                self.wait_window(self.confirmPopup)
                if self.confirmPopup.ans:
                    delete_trail(conn, trail_name)
                else:
                    conn.close()
                    return False

        elif not deleting and not insert_trail(conn, trail_name, county, state):
            self.errorMessage.configure(text="Trail already exists in database!")
            self.errorMessage.pack()
            conn.close()
            return False

        conn.close()
        s = "Your trail has been\nsuccessfully added to\nyour trail database!"
        if deleting:
            s = "Your trail has been\nsuccessfully deleted from\nyour trail database!"
        self.successBox = Popup(self, title="Success!", text=s,
                                width=self.sizes.width // 3, height=self.sizes.height // 4)
        return True


    def key_press(self, event=None):
        self.errorMessage.pack_forget()
        if event is not None and event.keycode == 13 and event.state != 1: # enter
            self.validate_trail_input()
        elif event is not None and event.keycode == 13 and event.state == 1: # shift + enter
            self.validate_trail_input(True)
        elif event is not None and event.keycode == 27: # esc
            self.master.close_popup()


    def success_box_close(self):
        self.successBox.destroy()
        self.successBox = None


    def format_county(self, county) -> str:
        # make sure county ends with "County"
        if county.endswith("county"):
            county = county[:-6]
            county += "County"
        if not county.endswith("County"):
            county += " County"
        county = county[0].upper() + county[1:]
        return county


    def close_all(self):
        self.master.close_all()


    def get_sizes(self):
        return self.sizes


    def get_settings(self):
        return self.settings