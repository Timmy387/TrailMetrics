import customtkinter as ctk
from GUI.MyCtkObjects.dateRangeFrame import DateRangeFrame
from GUI.MyCtkObjects.trailSelectFrame import TrailSelectFrame
from GUI.MyCtkObjects.gridDropdown import GridDropdown


class GraphInfo(ctk.CTkFrame):
    def __init__(self, master, og_master):
        super().__init__(master)
        self.og_master = og_master
        self.sizes = og_master.get_sizes()
        self.settings = og_master.get_settings()
        self.conn = og_master.get_conn()

        self.totalOrAvg = self.settings.total_or_avg()
        self.cmpTrailsOrDates = self.settings.cmp_trails_or_dates()

        self.configure(fg_color="transparent")
        self.months = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']


        # global options
        self.globalOptionsFrame = ctk.CTkFrame(master=self, fg_color="transparent")

        self.trailFrameGlobal = TrailSelectFrame(self.globalOptionsFrame, self.og_master,
                                                 self.sizes.font3_8, self.sizes.font3_8,
                                                 text="Trail:", side=True)


        # select by hour, day, week, month, year, or all time
        self.units = ["Time of Day", "Day of Week",
                      "Day of Year",
                      "Week", "Month", "Year"]
        self.smallUnitFrame = ctk.CTkFrame(master=self.globalOptionsFrame, fg_color="transparent")
        self.smallUnitLabel = ctk.CTkLabel(master=self.smallUnitFrame, text="Avg users\nper",
                                           font=self.sizes.font3_8)
        self.smallUnitLabel.pack(anchor="w", side="left", padx=self.sizes.padx // 3)
        self.smallUnitDropdown = GridDropdown(master=self.smallUnitFrame, og_master=self, cols=1,
                                              font=self.sizes.font3_8,
                                              dropdown_font=(self.sizes.font3_8[0], self.sizes.font3_8[1] - 1),
                                              width=self.sizes.width // 12)
        self.smallUnitDropdown.set("Month")
        self.smallUnitDropdown.pack()

        self.bigUnitFrame = ctk.CTkFrame(master=self.globalOptionsFrame, fg_color="transparent")
        self.bigUnitLabel = ctk.CTkLabel(master=self.bigUnitFrame, font=self.sizes.font3_8, text="each")
        self.bigUnitLabel.pack(anchor="w", side="left", padx=self.sizes.padx // 3)
        self.bigUnitDropdown = GridDropdown(master=self.bigUnitFrame, og_master=self, cols=1, values=self.units[3:],
                                            command=self.big_build_units, font=self.sizes.font3_8,
                                            dropdown_font=(self.sizes.font3_8[0], self.sizes.font3_8[1] - 1),
                                            width=self.sizes.width // 12)
        self.bigUnitDropdown.set("Year")
        self.bigUnitDropdown.pack()


        self.numConfigs = 1
        self.addRemoveFrame = ctk.CTkFrame(master=self.globalOptionsFrame, fg_color="transparent")
        self.addRemoveLabel = ctk.CTkLabel(master=self.addRemoveFrame,
                                            font=self.sizes.font3_8)
        self.addRemoveLabel.pack(side="left", padx=self.sizes.padx // 3)
        self.addConfig = ctk.CTkButton(master=self.addRemoveFrame, text="Add",
                                       width=self.sizes.width // 20, height=self.sizes.height // 24,
                                       command=self.add_config, font=self.sizes.font3_8)
        self.addConfig.pack(side="left", padx=self.sizes.padx // 3)
        self.removeConfig = ctk.CTkButton(master=self.addRemoveFrame, text="Remove",
                                          width=self.sizes.width // 20, height=self.sizes.height // 24,
                                          command=self.remove_config, font=self.sizes.font3_8)
        self.removeConfig.configure(state="disabled")
        self.removeConfig.pack(side="left", padx=self.sizes.padx // 3)
        self.addRemoveFrame.grid(row=0, column=3, padx=self.sizes.padx // 2)

        self.globalOptionsFrame.grid(row=0, column=1, padx=self.sizes.padx)

        unit = self.smallUnitDropdown.get().lower()
        self.dateRangeFrameGlobal = DateRangeFrame(master=self.globalOptionsFrame,
                                                   og_master=self.og_master, unit=unit)


        # multiple graphs options
        self.multiGraphFrame = ctk.CTkFrame(master=self, fg_color="transparent",
                                            width=int(self.sizes.width * 0.95), height=int(self.sizes.height * 0.1))

        trail_font = (self.sizes.font, self.sizes.font4_8[1] - 2)
        self.trailFrames = [TrailSelectFrame(self.multiGraphFrame, self.og_master, trail_font, self.sizes.font3_8,
                            text="Trail 1:", side=True, fg_color="purple"),
                            TrailSelectFrame(self.multiGraphFrame, self.og_master, trail_font, self.sizes.font3_8,
                            text="Trail 2:", side=True, fg_color="red"),
                            TrailSelectFrame(self.multiGraphFrame, self.og_master, trail_font, self.sizes.font3_8,
                            text="Trail 3:", side=True, fg_color="orange"),
                            TrailSelectFrame(self.multiGraphFrame, self.og_master, trail_font, self.sizes.font3_8,
                            text="Trail 4:", side=True, fg_color="green")]

        self.dateRangeFrames = [DateRangeFrame(master=self.multiGraphFrame, og_master=self.og_master, unit=unit, color="purple"),
                                DateRangeFrame(master=self.multiGraphFrame, og_master=self.og_master, unit=unit, color="red"),
                                DateRangeFrame(master=self.multiGraphFrame, og_master=self.og_master, unit=unit, color="orange"),
                                DateRangeFrame(master=self.multiGraphFrame, og_master=self.og_master, unit=unit, color="green")]
        self.build_frame()


    def reset(self):
        self.numConfigs = 1
        self.addConfig.configure(state="normal")
        self.removeConfig.configure(state="disabled")
        self.redraw_multi_frame()
        self.smallUnitDropdown.set("Month")
        self.bigUnitDropdown.set("Year")
        self.trailFrameGlobal.reset()
        self.dateRangeFrameGlobal.reset()
        for i in range(4):
            self.trailFrames[i].reset()
            self.dateRangeFrames[i].reset()

    def get_config(self):
        totoravg, cmptord = self.get_switches()
        graph_description = {
            "totalOrAvg": totoravg,
            "cmpTrailsOrDates": cmptord,
            "smallUnit": self.smallUnitDropdown.get(),
            "bigUnit": self.bigUnitDropdown.get(),
            "numConfigurations": self.numConfigs,
            "globalTrail": self.trailFrameGlobal.get(),
            "globalDateRange": self.dateRangeFrameGlobal.get_date(),
            "trailConfigs": [self.trailFrames[i].get() for i in range(self.numConfigs)],
            "dateRangeConfigs": [self.dateRangeFrames[i].get_date() for i in range(self.numConfigs)]
        }
        return graph_description


    def get_sizes(self):
        return self.sizes


    def get_switches(self):
        return self.settings.total_or_avg(), self.settings.cmp_trails_or_dates()


    def build_frame(self, event=None):
        self.forget_all()
        self.totalOrAvg, self.cmpTrailsOrDates = self.get_switches()
        if self.totalOrAvg == 1:
            self.smallUnitLabel.configure(text="Average\nusers per")
        else:
            self.smallUnitLabel.configure(text="Total\nusers per")
        self.smallUnitFrame.grid(row=0, column=1)
        self.bigUnitFrame.grid(row=0, column=2)
        self.big_build_units()
        self.trailFrameGlobal.reset()
        for frame in self.trailFrames:
            frame.reset()

        if self.cmpTrailsOrDates == 1:
            self.addRemoveLabel.configure(text="Add/Remove\nDate ranges:")
            self.trailFrameGlobal.grid(row=0, column=0, padx=self.sizes.padx)
        else:
            self.addRemoveLabel.configure(text="Add/Remove\nTrails:")
            self.dateRangeFrameGlobal.grid(row=0, column=0, padx=self.sizes.padx)
        self.redraw_multi_frame()


    def big_build_units(self, event=None):
        unit = self.bigUnitDropdown.get()
        smallUnit = self.smallUnitDropdown.get()
        values = self.units[:self.units.index(unit) - 1]
        if unit == "Year":
            values.append("Month")
        self.smallUnitDropdown.set_values(values=values)
        if smallUnit not in values:
            self.smallUnitDropdown.set(values[-1])
        self.dateRangeFrameGlobal.refresh(unit.lower())
        for dateRangeFrame in self.dateRangeFrames:
            dateRangeFrame.refresh(unit.lower())


    def forget_all(self):
        self.smallUnitFrame.grid_forget()
        self.bigUnitFrame.grid_forget()
        self.trailFrameGlobal.grid_forget()
        self.dateRangeFrameGlobal.grid_forget()


    def redraw_multi_frame(self):
        self.multiGraphFrame.grid_forget()
        for trailFrame in self.trailFrames:
            trailFrame.grid_forget()
        for dateRangeFrame in self.dateRangeFrames:
            dateRangeFrame.grid_forget()
        cmptord = self.settings.cmp_trails_or_dates()
        tempDatesOrTrailsArr = self.dateRangeFrames if cmptord == 1 else self.trailFrames
        for i in range(self.numConfigs):
            if self.numConfigs == 3 and i == 2:
                tempDatesOrTrailsArr[i].grid(row=1, column=0, columnspan=2, pady=self.sizes.pady, padx=self.sizes.padx)
            else:
                tempDatesOrTrailsArr[i].grid(row=i // 2, column=i % 2, pady=self.sizes.pady, padx=self.sizes.padx)
        self.multiGraphFrame.grid(row=1, column=1)


    def add_config(self):
        if self.numConfigs == 1:
            self.removeConfig.configure(state="normal")
        if self.numConfigs < 4:
            self.numConfigs += 1
            self.redraw_multi_frame()
        if self.numConfigs == 4:
            self.addConfig.configure(state="disabled")


    def remove_config(self):
        if self.numConfigs == 4:
            self.addConfig.configure(state="normal")
        if self.numConfigs > 1:
            self.numConfigs -= 1
            self.redraw_multi_frame()
        if self.numConfigs == 1:
            self.removeConfig.configure(state="disabled")

    def current_location(self):
        return self.master.current_location()


    def get_settings(self):
        return self.settings


    def click(self, event=None):
        for frame in self.dateRangeFrames:
            frame.click(event)
        self.dateRangeFrameGlobal.click(event)
        if not self.smallUnitDropdown.dropdown_button_clicked(event):
            self.smallUnitDropdown.close_dropdown()
        if not self.bigUnitDropdown.dropdown_button_clicked(event):
            self.bigUnitDropdown.close_dropdown()