import customtkinter as ctk
from customtkinter import CTkToplevel

from GUI.MyCtkObjects.optionDropdown import OptionDropdown
from GUI.Screens.editTrails import EditTrails
from GUI.Screens.importDataPopup import ImportData
from GUI.Screens.settingsPopup import SettingsPopup
from GUI.MyCtkObjects.popup import Popup
from SQLiteFiles.DatabaseQueries.trails_queries import list_trails
from GUI.graphInfo import GraphInfo
from GUI.MyCtkObjects.graphBuilder import GraphBuilder


class StartScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.og_master = master
        self.sizes = master.get_sizes()
        self.settings = master.get_settings()
        self.conn = master.get_conn()

        self.optionsDropdown = OptionDropdown(master=self, og_master=self.og_master, label="Options", corner_radius=5,
                                              font=self.sizes.font4_8, dropdown_font=("Roboto", self.sizes.font3_8[1]),
                                              width=self.sizes.width // 12, dropdown_width=self.sizes.width // 5,
                                              values=["Draw graph", "Save graph", "Upload file", "Edit trails",
                                                   "Settings", "Clear config", "Help", "Close window"],
                                              commands=[self.build_graphs, self.save_graph,
                                                        lambda: self.open_popup(ImportData),
                                                        lambda: self.open_popup(EditTrails),
                                                        lambda: self.open_popup(SettingsPopup),
                                                        self.clear_config, self.help, self.close_all],
                                              shortcuts=["Ctrl+D", "Ctrl+S", "Ctrl+U", "Ctrl+E",
                                                         "Ctrl+Shift+S", "Ctrl+C", "Ctrl+H", "Ctrl+Q"])
        self.optionsDropdown.place(x=0, y=0, anchor="nw", relx=0.01, rely=0.01)

        self.graphInfoBlock = GraphInfo(self, self)
        self.graphInfoBlock.pack(pady=self.sizes.pady)

        self.graphBuilder = GraphBuilder(self, self.og_master, self.graphInfoBlock.get_config())
        self.graphBuilder.pack(padx=self.sizes.pady * 2, expand=True, fill="both")

        self.popup = None
        creds = """
Trail Metrics App: No rights reserved, use it for whatever ya want. I mean what would you do \
with it anyway lol. Thanks for using it! -Timmy Boyce
"""
        self.credits = ctk.CTkLabel(master=self, text=creds, font=(self.sizes.font, 10), text_color="gray", anchor="e")
        self.credits.pack(side="bottom", anchor="e", padx=self.sizes.padx // 2)


    def open_popup(self, popup_class):
        if popup_class == ImportData:
            if not list_trails(self.conn):
                at = Popup(self, "No trails exist", "Add a trail first!", yesno=True,
                           yes="Add Trail", no="Later", width=self.sizes.width // 3, height=self.sizes.height // 6)
                self.wait_window(at)
                if at.ans:
                    self.open_popup(EditTrails)
                return
        self.popup = popup_class(self)


    def close_popup(self):
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None
        # self.popup.withdraw()
        # self.grab_set()


    def switch_popup(self, popup_class):
        self.close_popup()
        self.open_popup(popup_class)


    def close_all(self, reopen=False):
        self.master.close_all(reopen)


    def get_settings(self):
        return self.settings


    def get_sizes(self):
        return self.sizes


    def get_conn(self):
        return self.master.get_conn()


    def refresh_scheme(self):
        self.master.refresh_scheme()


    def build_graphs(self, event=None, popup=True):
        self.graphBuilder.update_config(self.graphInfoBlock.get_config())
        self.graphBuilder.build_graph(popup=popup)


    def clear_config(self):
        self.graphBuilder.clear_graph()
        self.graphInfoBlock.reset()


    def save_graph(self):
        self.graphBuilder.save()


    def current_location(self):
        return self.master.current_location()


    def build_graph_info(self, event=None):
        self.graphInfoBlock.build_frame()

    def click(self, event=None):
        self.graphInfoBlock.click(event)
        if not self.optionsDropdown.dropdown_btn_clicked(event):
            self.optionsDropdown.close_dropdown()

    def help(self):
        helpText = """
Not implemented yet, sorry!
You will have to just 
figure it out on your own,
good luck lol.
Go to:
        """
        link = "Github.com/Timmy387/TrailMetrics/blob/main/README.md"
        readmore = "to read at least a little about the app."
        popup = CTkToplevel(self)
        x = self.sizes.screenWidth // 2
        y = self.sizes.screenHeight // 2 - self.sizes.height // 4
        popup.geometry(f"{int(self.sizes.width // 3)}x{self.sizes.height // 3}+{x}+{y}")
        popup.title("Help")
        popup.attributes("-topmost", True)
        popup.resizable(False, False)
        popup.grab_set()
        helpLabel = ctk.CTkLabel(master=popup, text=helpText, font=self.sizes.font4_8)
        helpLabel.pack(padx=self.sizes.padx)
        linkBox = ctk.CTkTextbox(master=popup, width=int(self.sizes.width // 2.9), height=self.sizes.height // 20,
                                        font=self.sizes.font3_8, scrollbar_button_color=None)
        linkBox.insert("0.0", link)
        linkBox.configure(state="disabled")
        linkBox.configure(bg_color="transparent", fg_color="transparent", border_width=0)
        linkBox._textbox.tag_configure("center", justify="center")
        linkBox.tag_add("center", "1.0", "end")
        linkBox.pack(padx=self.sizes.padx // 2, ipady=0, pady=0)
        readmoreLabel = ctk.CTkLabel(master=popup, text=readmore, font=self.sizes.font4_8)
        readmoreLabel.pack()


        # popup = Popup(self, "Help", helpText, yesno=False)
        # self.wait_window(popup)