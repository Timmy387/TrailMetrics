import customtkinter as ctk
from connect_sqlite import connect_trail_db_sqlite
from SQLiteFiles.DDL.inserts import insert_trail, delete_trail
from GUI.popup import Popup


class AddTrail(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.returnBtn = ctk.CTkButton(master=self, text="Return to\nmain menu", command=self.master.rtn,
                                         width=60, height=20, font=("Roboto", 20))
        self.returnBtn.place(relx=1.0, rely=1.0, anchor=ctk.SE, x=-20, y=-20)

        self.labelFrame = ctk.CTkFrame(master=self, border_width=2, width=600, height=150)
        self.labelFrame.pack(pady=40, padx=10)

        self.addTrailLabel = ctk.CTkLabel(master=self.labelFrame, text="Add a trail by filling\nin the info below!",
                                          font=("Roboto", 35))
        self.addTrailLabel.pack(pady=10, padx=10)

        self.trailNameInput = ctk.CTkEntry(master=self, placeholder_text="Trail name", font=("Roboto", 30), width=300)
        self.trailNameInput.pack(pady=15)

        self.countyInput = ctk.CTkEntry(master=self, placeholder_text="County", font=("Roboto", 30), width=300)
        self.countyInput.pack(pady=15)

        self.states = [
                "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
            ]

        def on_validate_input(P):
            P = P.upper()
            # Allow only up to 2 characters
            if len(P) <= 2:
                return True
            return False

        vcmd = (self.register(on_validate_input), "%P")
        self.stateInput = ctk.CTkEntry(master=self, placeholder_text="St", font=("Roboto", 30),
                                       width=300, validate="key", validatecommand=vcmd)
        self.stateInput.pack(pady=15)

        self.buttonFrame = ctk.CTkFrame(master=self)

        self.enterTrailBtn = ctk.CTkButton(master=self.buttonFrame, text="Enter new trail!", width=280, height=70,
                                           font=("Roboto", 35), command=self.validate_trail_input)
        self.enterTrailBtn.grid(row=0, column=0, padx=10, pady=10)

        self.deleteTrailBtn = ctk.CTkButton(master=self.buttonFrame, text="Delete old trail!", width=280, height=70,
                                           font=("Roboto", 35), command=lambda: self.validate_trail_input(True))
        self.deleteTrailBtn.grid(row=0, column=1, padx=10, pady=10)

        self.buttonFrame.pack(pady=20)

        self.noTrailError = ctk.CTkLabel(master=self, text="Please enter a trail name to delete!", font=("Roboto", 20),
                                         text_color="red")

        self.fillAllError = ctk.CTkLabel(master=self, text="Please fill in all fields!", font=("Roboto", 20),
                               text_color="red")

        self.notAState = ctk.CTkLabel(master=self, font=("Roboto", 20), text_color="red")

        self.dbError = ctk.CTkLabel(master=self, text="Database insertion failure.", font=("Roboto", 20), text_color="red")

        self.trailExistsError = ctk.CTkLabel(master=self, text="Trail already exists in database!", font=("Roboto", 20),
                                             text_color="red")

        self.trailDoesNotExistError = ctk.CTkLabel(master=self, text="Trail does not exist in database!", font=("Roboto", 20),
                                                   text_color="red")

        self.successBox = None

        self.master.bind("<KeyPress>", func=self.eraseResults)


    def validate_trail_input(self, deleting=False) -> bool:
        self.eraseResults()
        trail_name = self.trailNameInput.get()
        state = self.stateInput.get()
        county = self.countyInput.get()
        if deleting and len(trail_name) == 0:
            self.noTrailError.pack(pady=0)
            return False

        elif not deleting and (len(trail_name) == 0 or len(county) == 0 or len(state) == 0):
            self.fillAllError.pack(pady=0)
            return False

        elif not deleting and state.upper() not in self.states:
            self.notAState.configure(text=f"{self.stateInput.get().upper()} is not a US state!")
            self.notAState.pack(pady=0)
            return False

        conn = connect_trail_db_sqlite()
        if deleting:
            if not delete_trail(conn, trail_name):
                self.trailDoesNotExistError.pack(pady=10)
                conn.close()
                return False
        else:
            if not insert_trail(conn, trail_name, county, state):
                self.trailExistsError.pack(pady=10)
                conn.close()
                return False
        conn.close()
        s = "Your trail has been\nsuccessfully added to\nyour trail database!"
        w = 350
        if deleting:
            s = "Your trail has been\nsuccessfully deleted from\nyour trail database!"
            w = 400
        self.successBox = Popup(self, title="Success!", text=s, width=w, height=200)
        self.successBox.center()

        return True


    def eraseResults(self, event=None):
        self.fillAllError.pack_forget()
        self.notAState.pack_forget()
        self.dbError.pack_forget()
        self.trailExistsError.pack_forget()
        self.trailDoesNotExistError.pack_forget()
        self.noTrailError.pack_forget()
        if event is not None and event.keycode == 13 and event.state != 1:
            self.validate_trail_input()
        elif event is not None and event.keycode == 13 and event.state == 1:
            self.validate_trail_input(True)

    def on_close(self):
        self.successBox.destroy()
        self.successBox = None