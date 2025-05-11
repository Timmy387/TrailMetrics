import customtkinter as ctk
from tkinter import filedialog
from GUI.MyCtkObjects.inputField import InputField
from GUI.MyCtkObjects.popup import Popup
from SQLiteFiles.DDL.upload_file import upload, remove_file_values_trail_user
from SQLiteFiles.DatabaseQueries.files_queries import is_file
from SQLiteFiles.DatabaseQueries.trails_queries import is_trail, list_trails
from GUI.MyCtkObjects.trailSelectFrame import TrailSelectFrame


class ImportData(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.sizes = master.get_sizes()
        self.settings = master.get_settings()
        self.conn = master.get_conn()
        self.transient(master)
        self.grab_set()

        self.title("Import Data")
        self.geometry(f"{self.sizes.new_window_width}x{self.sizes.new_window_height}+"
                      f"{self.sizes.new_window_x}+{self.sizes.new_window_y}")
        self.resizable(False, False)

        self.labelFrame = ctk.CTkFrame(master=self, border_width=2)

        self.uploadFileLabel = ctk.CTkLabel(master=self.labelFrame, text="Upload a file to import data!",
                                          font=self.sizes.font_full)
        self.uploadFileLabel.pack(pady=self.sizes.pady, padx=self.sizes.padx)

        self.labelFrame.pack(pady=self.sizes.pady_title, padx=self.sizes.padx)

        self.trailFrame = TrailSelectFrame(self, self, label_font=self.sizes.font4_8, font=self.sizes.font6_8,
                                           width=int(self.sizes.width // 2.5), height=int(self.sizes.height // 16))
        self.trailFrame.pack(pady=self.sizes.pady)

        self.fileInputField = InputField(master=self, label_text="File path:", placeholder_text="File path",
                                         button=("Browse", self.open_file_dialog))
        self.fileInputField.pack(pady=self.sizes.pady)

        self.filePath = ""

        self.buttonFrame = ctk.CTkFrame(master=self, fg_color="transparent")

        self.uploadButton = ctk.CTkButton(master=self.buttonFrame, text="Upload file",
                                          command=self.upload_file,
                                          font=self.sizes.font7_8,
                                          width=int(self.sizes.width // 4.5), height=self.sizes.height // 9)
        self.uploadButton.grid(row=0, column=0, padx=self.sizes.padx, pady=self.sizes.pady * 2)

        self.removeButton = ctk.CTkButton(master=self.buttonFrame, text="Remove file\ncontents",
                                          command=self.remove_file_contents,
                                          font=self.sizes.font7_8,
                                          width=int(self.sizes.width // 4.5), height=self.sizes.height // 9)
        self.removeButton.grid(row=0, column=1, padx=self.sizes.padx, pady=self.sizes.pady * 2)

        self.closeBtn = ctk.CTkButton(master=self.buttonFrame, text="Close",
                                      width=self.sizes.width // 5, height=self.sizes.height // 12,
                                      font=self.sizes.font6_8,
                                      command=self.destroy)
        self.closeBtn.grid(row=1, column=0, columnspan=2, pady=self.sizes.pady * 2)

        self.buttonFrame.pack(pady=self.sizes.pady * 2, padx=self.sizes.padx)

        self.errorMessage = ctk.CTkLabel(master=self, font=self.sizes.font4_8, text_color="red")

        self.bind("<KeyPress>", self.key_press)
        self.bind("<Button-1>", self.focus_out)

    def focus_out(self, event):
        for child in self.fileInputField.input.winfo_children():
            if event.widget == child:
                return
        for child in self.trailFrame.winfo_children():
            if event.widget == child:
                return
        self.focus_set()


    def open_file_dialog(self):
        fileInput = filedialog.askopenfilename(title="Select a text file to upload",
                                               filetypes=[("TXT files", "*.txt")])
        if fileInput:
            self.filePath = fileInput
            self.fileInputField.insert(fileInput)


    def upload_file(self):
        trail = self.trailFrame.get()
        if trail == "Choose":
            self.errorMessage.configure(text="Please select a trail!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        trail_name, county, state = self.split_trail_entry()
        if not self.filePath:
            self.errorMessage.configure(text="Please select a file to upload!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        trail_name = self.format_trail(trail_name)
        if not is_trail(self.conn, trail_name, county, state):
            self.errorMessage.configure(text="Trail does not exist!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        if is_file(self.conn, self.filePath):
            self.errorMessage.configure(text="File with this name has already been uploaded!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        elif not upload(self.conn, trail_name, county, state, self.filePath):
            # TODO: check that it is the right kind of file
            self.errorMessage.configure(text="File contains duplicate data!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        popup = Popup(self, title="Success!", text="File uploaded successfully!")
        self.wait_window(popup)


    def remove_file_contents(self):
        trail = self.trailFrame.get()
        if trail == "Choose":
            self.errorMessage.configure(text="Please select a trail!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        trail_name, county, state = self.split_trail_entry()
        path = self.fileInputField.get()
        if not is_trail(self.conn, trail_name, county, state):
            self.errorMessage.configure(text="Trail does not exist!")
            self.errorMessage.pack(pady=self.sizes.pady)
        if not path:
            self.errorMessage.configure(text="Please select a file to remove!")
            self.errorMessage.pack(pady=self.sizes.pady)
        if not is_file(self.conn, path):
            self.errorMessage.configure(text="File does not exist!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        if not remove_file_values_trail_user(self.conn, path, trail_name, county, state):
            self.errorMessage.configure(text="File does not exist!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        self.errorMessage.configure(text="File contents removed successfully!")
        self.errorMessage.pack(pady=self.sizes.pady)


    def key_press(self, event=None):
        self.errorMessage.pack_forget()
        if event is not None and event.keycode == 13 and event.state != 1: # enter
            self.upload_file()
        # elif event is not None and event.keycode == 13 and event.state == 1: # shift + enter
        #     self.remove_file_contents()
        elif event is not None and event.keycode == 27: # esc
            self.master.close_popup()


    def format_trail(self, trail_name):
        trail_name = trail_name[0].upper() + trail_name[1:]
        return trail_name


    def split_trail_entry(self):
        trail = self.trailFrame.get().split(", ")
        trail_name = trail[0]
        county = trail[1]
        state = trail[2]
        return trail_name, county, state


    def get_settings(self):
        return self.settings


    def get_sizes(self):
        return self.sizes


    def get_conn(self):
        return self.conn

    def close_all(self):
        self.master.close_all()