import customtkinter as ctk

from SQLiteFiles.DatabaseQueries.trails_queries import is_trail
from SQLiteFiles.DDL.inserts import insert_trail, delete_trail
from SQLiteFiles.DatabaseQueries.county_queries import is_state, is_county_in_state
from GUI.MyCtkObjects.popup import Popup
from GUI.MyCtkObjects.inputField import InputField


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
        self.conn = master.get_conn()
        self.transient(master)
        self.grab_set()
        self.title("Add Trail")
        self.geometry(f"{self.sizes.new_window_width}x{self.sizes.new_window_height}+"
                      f"{self.sizes.new_window_x}+{self.sizes.new_window_y}")
        self.resizable(False, False)

        self.labelFrame = ctk.CTkFrame(master=self, border_width=2)

        self.addTrailLabel = ctk.CTkLabel(master=self.labelFrame, text="Add a trail by\nfilling in the info below!",
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


        self.enterTrailBtn = ctk.CTkButton(master=self, text="Enter new trail",
                                           width=int(self.sizes.width // 4), height=self.sizes.height // 12,
                                           font=self.sizes.font_full, command=self.validate_trail_input)
        self.enterTrailBtn.pack(pady=self.sizes.pady * 2)

        self.closeBtn = ctk.CTkButton(master=self, text="Close",
                                      width=self.sizes.width // 5, height=self.sizes.height // 16,
                                      font=self.sizes.font_full,
                                      command=self.master.close_popup)
        self.closeBtn.pack(pady=self.sizes.pady)

        self.errorMessage = ctk.CTkLabel(master=self, font=self.sizes.font4_8,text_color="red")

        self.successBox = None

        self.bind("<KeyPress>", func=self.key_press)
        self.bind("<Button-1>", self.focus_out)

    def focus_out(self, event):
        for child in self.trailNameInput.input.winfo_children():
            if event.widget == child:
                return
        for child in self.countyInput.input.winfo_children():
            if event.widget == child:
                return
        for child in self.stateInput.input.winfo_children():
            if event.widget == child:
                return
        self.focus_set()



    def validate_trail_input(self, deleting=False) -> bool:
        self.errorMessage.pack_forget()
        trail_name = self.trailNameInput.get()
        state = self.stateInput.get().upper()
        county = self.format_county(self.countyInput.get())
        success = True
        if len(trail_name) == 0 or len(county) == 0 or len(state) == 0:
            self.errorMessage.configure(text="Please fill in all fields.")
            self.errorMessage.pack()
            success = False

        elif not is_state(self.conn, state):
            self.errorMessage.configure(text=f"{self.stateInput.get().upper()} is not a US state.")
            self.errorMessage.pack()
            success = False

        elif not is_county_in_state(self.conn, county, state):
            self.errorMessage.configure(text=f"{county} is not a county in {state.upper()}.")
            self.errorMessage.pack()
            success = False

        elif not insert_trail(self.conn, trail_name, county, state):
            self.errorMessage.configure(text="Trail already exists in database.")
            self.errorMessage.pack()
            success = False

        self.after(3000, lambda: self.errorMessage.pack_forget())
        if not success:
            return False
        s = "Your trail has been\nsuccessfully added to\nyour trail database."
        self.successBox = Popup(self, title="Success!", text=s)
        return True


    def key_press(self, event=None):
        if event is not None and event.keycode == 13 and event.state != 1: # enter
            self.validate_trail_input()
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