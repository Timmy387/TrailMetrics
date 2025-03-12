import customtkinter as ctk
from tkinter import filedialog
from GUI2.inputField import InputField
from SQLiteFiles.DDL.upload_file import upload
from connect_sqlite import connect_trail_db_sqlite
from SQLiteFiles.DatabaseQueries.trails_queries import is_trail


class ImportData(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.sizes = master.get_sizes()
        self.settings = master.get_settings()
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

        self.trailNameInput = InputField(master=self, label_text="Trail name:", placeholder_text="Trail name")
        self.trailNameInput.pack(pady=self.sizes.pady)
        # self.trailNameInput.focus_set()
        self.after(50, self.trailNameInput.focus_set)

        self.fileInputField = InputField(master=self, label_text="File path:", placeholder_text="File path",
                                         button=("Browse", self.open_file_dialog))
        self.fileInputField.pack(pady=self.sizes.pady)

        self.filePath = ""

        self.uploadButton = ctk.CTkButton(master=self, text="Upload file", command=self.upload_file, font=self.sizes.font6_8,
                                          width=self.sizes.width // 6, height=self.sizes.height // 16)
        self.uploadButton.pack(pady=self.sizes.pady * 5)

        self.errorMessage = ctk.CTkLabel(master=self, font=self.sizes.font4_8, text_color="red")

        self.bind("<KeyPress>", self.key_press)


    def open_file_dialog(self):
        fileInput = filedialog.askopenfilename(title="Select a text file to upload",
                                               filetypes=[("TXT files", "*.txt")])
        if fileInput:
            self.filePath = fileInput
            self.fileInputField.insert(fileInput)


    def upload_file(self):
        conn = connect_trail_db_sqlite()
        trail_name = self.trailNameInput.get()
        if not trail_name:
            self.errorMessage.configure(text="Please enter a trail name!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        elif not self.filePath:
            self.errorMessage.configure(text="Please select a file to upload!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        trail_name = self.format_trail(self.trailNameInput.get())
        if not is_trail(conn, trail_name):
            self.errorMessage.configure(text="Trail does not exist!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        elif not upload(conn, trail_name, self.filePath):
            # TODO: check that it is the right kind of file
            self.errorMessage.configure(text="File upload failed!")
            self.errorMessage.pack(pady=self.sizes.pady)
            return
        # TODO: success popup
        self.errorMessage.configure(text="File uploaded successfully!")


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


    def get_settings(self):
        return self.settings


    def get_sizes(self):
        return self.sizes

    def close_all(self):
        self.master.close_all()