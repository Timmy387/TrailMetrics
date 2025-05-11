import customtkinter as ctk
from datetime import date
from GUI.MyCtkObjects.gridDropdown import GridDropdown


class DateRangeFrame(ctk.CTkFrame):
    def __init__(self, master, og_master=None, unit=None, color=None):
        super().__init__(master)
        self.sizes = og_master.get_sizes()
        self.settings = og_master.get_settings()
        self.og_master = og_master
        self.unit = unit
        self.configure(fg_color="transparent")
        self.months = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
        self.today = date.today()

        self.corner_radius = 0
        if color is not None:
            self.color = color
        else:
            self.color = ctk.ThemeManager.theme["CTkLabel"]["text_color"]
        self.dropdownFont = (self.sizes.font3_8[0], self.sizes.font3_8[1] - 1)

        # start date frame
        self.startDateFrame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.startDateLabel = ctk.CTkLabel(master=self.startDateFrame, text_color=self.color,
                                           text="From", font=(self.sizes.font, self.sizes.font4_8[1] - 2))
        self.startDateLabel.grid(row=0, column=0, padx=self.sizes.padx // 3)

        self.yearDropdownStart = GridDropdown(master=self.startDateFrame, og_master=self,
                                              cols=4, font=self.sizes.font3_8,
                                              dropdown_font=self.dropdownFont, command=self.set_start_before_end,
                                              corner_radius=self.corner_radius)


        self.monthDropdownStart = GridDropdown(master=self.startDateFrame, og_master=self,
                                               cols=3, font=self.sizes.font3_8,
                                               dropdown_font=self.dropdownFont, command=self.set_start_before_end,
                                               corner_radius=self.corner_radius, width=round(self.sizes.width / 16))

        self.dayDropdownStart = GridDropdown(master=self.startDateFrame, og_master=self,
                                             cols=5, font=self.sizes.font3_8,
                                             dropdown_font=self.dropdownFont, command=self.set_start_before_end,
                                             corner_radius=self.corner_radius, width=self.sizes.width // 30)


        # end date frame
        self.endDateFrame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.endDateLabel = ctk.CTkLabel(master=self.endDateFrame, text_color=self.color,
                                         text="To", font=(self.sizes.font, self.sizes.font4_8[1] - 2))
        self.endDateLabel.grid(row=0, column=0, padx=self.sizes.padx // 3)

        self.yearDropdownEnd = GridDropdown(master=self.endDateFrame, og_master=self,
                                            cols=4, font=self.sizes.font3_8,
                                            dropdown_font=self.dropdownFont, command=self.set_end_after_start,
                                            corner_radius=self.corner_radius)

        self.monthDropdownEnd = GridDropdown(master=self.endDateFrame, og_master=self,
                                             cols=3, font=self.sizes.font3_8,
                                             dropdown_font=self.dropdownFont, command=self.set_end_after_start,
                                             corner_radius=self.corner_radius, width=round(self.sizes.width / 16))

        self.dayDropdownEnd = GridDropdown(master=self.endDateFrame, og_master=self,
                                           cols=5, font=self.sizes.font3_8,
                                           dropdown_font=self.dropdownFont, command=self.set_end_after_start,
                                           corner_radius=self.corner_radius, width=self.sizes.width // 30)


        self.yearDropdownStart.set_values(values=[str(i) for i in range(self.today.year - 19, self.today.year + 1)])
        self.yearDropdownEnd.set_values(values=[str(i) for i in range(self.today.year - 19, self.today.year + 1)])
        self.yearDropdownStart.set(str(self.today.year))
        self.yearDropdownEnd.set(str(self.today.year))

        self.start_dropdowns()

        self.monthDropdownStart.grid(row=0, column=1)
        self.dayDropdownStart.grid(row=0, column=2, padx=1)
        self.yearDropdownStart.grid(row=0, column=3)
        self.startDateFrame.grid(row=0, column=0)

        self.monthDropdownEnd.grid(row=0, column=1)
        self.dayDropdownEnd.grid(row=0, column=2, padx=1)
        self.yearDropdownEnd.grid(row=0, column=3)
        self.endDateFrame.grid(row=0, column=1)


    def reset(self):
        self.yearDropdownStart.set(str(self.today.year))
        self.yearDropdownEnd.set(str(self.today.year))
        self.monthDropdownStart.set(self.months[self.today.month - 1])
        self.monthDropdownEnd.set(self.months[self.today.month - 1])
        self.dayDropdownStart.set(str(self.today.day))
        self.dayDropdownEnd.set(str(self.today.day))
        self.start_dropdowns()
        
    
    def start_dropdowns(self, unit=None):
        if unit is not None:
            self.unit = unit

        self.monthDropdownStart.set_values(values=self.months)
        self.monthDropdownEnd.set_values(values=self.months)

        if unit != "year" and unit != "month":
            self.set_day_dropdowns()
        else:
            self.dayDropdownStart.set_values(values=["1"])
            self.dayDropdownEnd.set_values(values=["31"])
            self.dayDropdownStart.set("1")
            self.dayDropdownEnd.set("31")

        if unit is None:
            self.monthDropdownStart.set(self.months[self.today.month - 1])
            self.monthDropdownEnd.set(self.months[self.today.month - 1])
            self.dayDropdownStart.set(str(self.today.day))
            self.dayDropdownEnd.set(str(self.today.day))

        if self.unit == "year":
            self.monthDropdownStart.set_values(values=["January"])
            self.monthDropdownEnd.set_values(values=["December"])
            self.monthDropdownStart.set("January")
            self.monthDropdownEnd.set("December")
        if self.unit == "year" or self.unit == "month":
            self.dayDropdownStart.set_values(values=["1"])
            self.dayDropdownEnd.set_values(values=["31"])
            self.dayDropdownStart.set("1")
            self.dayDropdownEnd.set("31")


    def set_day_dropdowns(self, event=None):
        start_month = self.monthDropdownStart.get()
        start_day = self.dayDropdownStart.get()
        if self.unit == "year" or self.unit == "month":
            return
        if start_month == "February":
            start_days = [str(i) for i in range(1, 29)]
        elif start_month in ["April", "June", "September", "November"]:
            start_days = [str(i) for i in range(1, 31)]
        else:
            start_days = [str(i) for i in range(1, 32)]
        self.dayDropdownStart.set_values(values=start_days)
        if start_day not in start_days:
            self.dayDropdownStart.set(start_days[-1])

        end_month = self.monthDropdownEnd.get()
        end_day = self.dayDropdownEnd.get()
        if end_month == "February":
            end_days = [str(i) for i in range(1, 29)]
        elif end_month in ["April", "June", "September", "November"]:
            end_days = [str(i) for i in range(1, 31)]
        else:
            end_days = [str(i) for i in range(1, 32)]
        self.dayDropdownEnd.set_values(values=end_days)
        if end_day not in end_days:
            self.dayDropdownEnd.set(end_days[-1])


    def get_date(self):
        startYear, endYear = self.yearDropdownStart.get(), self.yearDropdownEnd.get()
        startMonth = self.months.index(self.monthDropdownStart.get()) + 1
        endMonth = self.months.index(self.monthDropdownEnd.get()) + 1
        startMonth, endMonth = str(startMonth).zfill(2), str(endMonth).zfill(2)
        start_date = f"{startYear}-{startMonth}-{self.dayDropdownStart.get().zfill(2)}"
        end_date = f"{endYear}-{endMonth}-{self.dayDropdownEnd.get().zfill(2)}"
        return start_date, end_date

    def build(self, unit):
        self.unit = unit
        if self.unit != "year" and self.unit != "month":
            self.start_dropdowns()


    def refresh(self, unit):
        self.unit = unit
        self.start_dropdowns(self.unit)


    def set_start_before_end(self, event=None):
        self.set_day_dropdowns()
        start_date = self.get_date()[0]
        end_date = self.get_date()[1]

        if start_date > end_date:
            self.yearDropdownEnd.set(self.yearDropdownStart.get())
            self.monthDropdownEnd.set(self.monthDropdownStart.get())
            self.dayDropdownEnd.set(self.dayDropdownStart.get())
        if self.unit == "year":
            self.monthDropdownEnd.set("December")
            self.dayDropdownEnd.set("31")
        if self.unit == "month":
            self.dayDropdownEnd.set("31")


    def set_end_after_start(self, event=None):
        self.set_day_dropdowns()
        start_date = self.get_date()[0]
        end_date = self.get_date()[1]

        if end_date < start_date:
            self.yearDropdownStart.set(self.yearDropdownEnd.get())
            self.monthDropdownStart.set(self.monthDropdownEnd.get())
            self.dayDropdownStart.set(self.dayDropdownEnd.get())
        if self.unit == "year":
            self.monthDropdownStart.set("January")
            self.dayDropdownStart.set("1")
        if self.unit == "month":
            self.dayDropdownStart.set("1")


    def get_sizes(self):
        return self.sizes


    def get_settings(self):
        return self.settings


    def current_location(self):
        return self.og_master.current_location()

    def click(self, event=None):
        date_dropdowns = [self.yearDropdownStart, self.monthDropdownStart, self.dayDropdownStart,
                          self.yearDropdownEnd, self.monthDropdownEnd, self.dayDropdownEnd]
        for dropdown in date_dropdowns:
            if not dropdown.dropdown_button_clicked(event):
                dropdown.close_dropdown()

