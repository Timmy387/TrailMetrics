import customtkinter as ctk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.category
# from matplotlib.category import StrCategoryConverter

from GUI.MyCtkObjects.popup import Popup
from SQLiteFiles.DatabaseQueries.total_trail_users_queries import per_month_each_year, \
    per_week_each_year, per_day_of_week_each_year, per_time_of_day_each_year, \
    per_day_of_year_each_year, per_day_of_year_each_month
from SQLiteFiles.DatabaseQueries import avg_trail_users_queries as avg_queries
from util import split_trail_entry
from tkinter import filedialog
from re import sub


# matplotlib.units.registry[object] = StrCategoryConverter()


class GraphBuilder(ctk.CTkFrame):
    def __init__(self, master, og_master, graph_description):
        super().__init__(master)
        self.conn = master.get_conn()
        self.og_master = og_master
        self.sizes = master.get_sizes()
        self.settings = master.get_settings()
        self.graphDescription = None
        self.graphTitle = ""
        self.xAxisLabel = ""
        self.yAxisLabel = ""
        self.xValues = []
        self.yValues = []
        self.colors = ["purple", "red", "orange", "green"]
        self.data = None
        self.trailGlobal = None
        self.dateRangeGlobal = None
        self.trailConfigs = None
        self.dateConfigs = None
        self.update_config(graph_description)

        if self.settings.theme() == "Dark":
            self.fontColor = "white"
            self.fig, self.ax = plt.subplots(facecolor='#1e1e1e')
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.widget = self.canvas.get_tk_widget()
            self.set_dark_mode()
        else:
            self.fontColor = "black"
            self.fig, self.ax = plt.subplots()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.widget = self.canvas.get_tk_widget()
        self.widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        # set title
        self.ax.set_title("Set The Fields Above And Click Build Graph In Options!", fontsize=13, color=self.fontColor)
        self.ax.set_xlabel("Timeframe", color=self.fontColor)
        self.ax.set_ylabel("Number of Users", color=self.fontColor)
        self.fig.subplots_adjust(left=0.08, right=0.95, top=0.91, bottom=0.1)
        self.canvas.draw()


    def update_config(self, graph_description):
        self.graphDescription = graph_description
        self.trailGlobal = split_trail_entry(self.graphDescription["globalTrail"])
        self.dateRangeGlobal = self.graphDescription["globalDateRange"]
        self.dateConfigs = []
        for i in range(self.graphDescription["numConfigurations"]):
            self.dateConfigs.append(self.graphDescription["dateRangeConfigs"][i])
        self.trailConfigs = []
        for i in range(self.graphDescription["numConfigurations"]):
            self.trailConfigs.append(split_trail_entry(self.graphDescription["trailConfigs"][i]))


    def choose_total_query_dates(self):
        trail_name, county, state = self.trailGlobal
        def build_data(query):
            self.data = []
            if self.graphDescription["numConfigurations"] > 1:
                self.graphTitle = (f"{trail_name} in {county}, {state}"
                                   f" total use per {self.graphDescription["smallUnit"].lower()} each"
                                   f" {self.graphDescription["bigUnit"].lower()}")
            else:
                self.graphTitle = (f"{trail_name} in {county}, {state}"
                                   f" from {self.dateConfigs[0][0]} to {self.dateConfigs[0][1]},"
                                   f" total use per {self.graphDescription["smallUnit"].lower()} each"
                                   f" {self.graphDescription["bigUnit"].lower()}")
            for start_date, end_date in self.dateConfigs:
                self.data.append(query(self.conn, trail_name, county, state, start_date, end_date))
        self.assign_total_query(build_data)


    def choose_total_query_trails(self):
        start_date, end_date = self.dateRangeGlobal
        def build_data(query):
            self.data = []
            if self.graphDescription["numConfigurations"] > 1:
                self.graphTitle = (f"{start_date}-{end_date}"
                                   f" total use per {self.graphDescription["smallUnit"].lower()} each"
                                   f" {self.graphDescription["bigUnit"].lower()}")
            else:
                self.graphTitle = (f"{start_date}-{end_date}"
                                   f" for {self.trailConfigs[0][0]}"
                                   f" total use per {self.graphDescription["smallUnit"].lower()} each"
                                   f" {self.graphDescription["bigUnit"].lower()}")
            for trail in self.trailConfigs:
                trail_name, county, state = trail
                self.data.append(query(self.conn, trail_name, county, state, start_date, end_date))
        self.assign_total_query(build_data)


    def assign_total_query(self, build_data):
        if self.graphDescription["bigUnit"] == "Year":
            if self.graphDescription["smallUnit"] == "Month":
                build_data(per_month_each_year)
            elif self.graphDescription["smallUnit"] == "Week":
                build_data(per_week_each_year)
            elif self.graphDescription["smallUnit"] == "Day of Year":
                build_data(per_day_of_year_each_year)
            elif self.graphDescription["smallUnit"] == "Day of Week":
                build_data(per_day_of_week_each_year)

            elif self.graphDescription["smallUnit"] == "Time of Day":
                build_data(per_time_of_day_each_year)

        elif self.graphDescription["bigUnit"] == "Month":
            if self.graphDescription["smallUnit"] == "Day of Year":
                build_data(per_day_of_year_each_month)

            elif self.graphDescription["smallUnit"] == "Day of Week":
                build_data(per_day_of_week_each_year)

            elif self.graphDescription["smallUnit"] == "Time of Day":
                build_data(per_time_of_day_each_year)

        elif self.graphDescription["bigUnit"] == "Week":
            if self.graphDescription["smallUnit"] == "Day of Week":
                build_data(per_day_of_week_each_year)

            elif self.graphDescription["smallUnit"] == "Time of Day":
                build_data(per_time_of_day_each_year)


    def choose_avg_query_dates(self):
        trail_name, county, state = self.trailGlobal
        def build_data(query):
            self.data = []
            if self.graphDescription["numConfigurations"] > 1:
                self.graphTitle = (f"{trail_name} in {county}, {state}"
                                   f" average use per {self.graphDescription["smallUnit"].lower()} each"
                                   f" {self.graphDescription["bigUnit"].lower()}")
            else:
                self.graphTitle = (f"{trail_name} in {county}, {state}"
                                   f" from {self.dateConfigs[0][0]} to {self.dateConfigs[0][1]},"
                                   f" average use per {self.graphDescription["smallUnit"].lower()} each"
                                   f" {self.graphDescription["bigUnit"].lower()}")
            for start_date, end_date in self.dateConfigs:
                self.data.append(query(self.conn, trail_name, county, state, start_date, end_date))

        self.assign_average_query(build_data)


    def choose_avg_query_trails(self):
        start_date, end_date = self.dateRangeGlobal

        def build_data(query):
            self.data = []
            if self.graphDescription["numConfigurations"] > 1:
                self.graphTitle = (f"{start_date}-{end_date}"
                                   f" average use per {self.graphDescription["smallUnit"].lower()} each"
                                   f" {self.graphDescription["bigUnit"].lower()}")
            else:
                self.graphTitle = (f"{start_date}-{end_date}"
                                   f" for {self.trailConfigs[0][0]}"
                                   f" average use per {self.graphDescription["smallUnit"].lower()} each"
                                   f" {self.graphDescription["bigUnit"].lower()}")
            for trail in self.trailConfigs:
                trail_name, county, state = trail
                self.data.append(query(self.conn, trail_name, county, state, start_date, end_date))

        self.assign_average_query(build_data)


    def assign_average_query(self, build_data):
        if self.graphDescription["bigUnit"] == "Year":
            if self.graphDescription["smallUnit"] == "Month":
                build_data(avg_queries.per_month_each_year)
            elif self.graphDescription["smallUnit"] == "Week":
                build_data(avg_queries.per_week_each_year)
            elif self.graphDescription["smallUnit"] == "Day of Year":
                build_data(avg_queries.per_day_of_year_each_year)
            elif self.graphDescription["smallUnit"] == "Day of Week":
                build_data(avg_queries.per_day_of_week_each_year)

            elif self.graphDescription["smallUnit"] == "Time of Day":
                build_data(avg_queries.per_time_of_day_each_year)

        elif self.graphDescription["bigUnit"] == "Month":
            if self.graphDescription["smallUnit"] == "Day of Year":
                build_data(avg_queries.per_day_of_year_each_month)

            elif self.graphDescription["smallUnit"] == "Day of Week":
                build_data(avg_queries.per_day_of_week_each_year)

            elif self.graphDescription["smallUnit"] == "Time of Day":
                build_data(avg_queries.per_time_of_day_each_year)

        elif self.graphDescription["bigUnit"] == "Week":
            if self.graphDescription["smallUnit"] == "Day of Week":
                build_data(avg_queries.per_day_of_week_each_year)

            elif self.graphDescription["smallUnit"] == "Time of Day":
                build_data(avg_queries.per_time_of_day_each_year)


    def choose_query(self):
        if self.graphDescription["totalOrAvg"] == 0:
            if self.graphDescription["cmpTrailsOrDates"] == 1:
                self.choose_total_query_dates()
            else:
                self.choose_total_query_trails()

        else:
            if self.graphDescription["cmpTrailsOrDates"] == 1:
                self.choose_avg_query_dates()
            else:
                self.choose_avg_query_trails()


        if self.graphTitle == "":
            self.graphTitle = "No query for this configuration yet."


    def validate_query(self, popup=True):
        if self.graphDescription["cmpTrailsOrDates"] == 1:
            trail_name, county, state = split_trail_entry(self.graphDescription["globalTrail"])
            if trail_name is None:
                if popup:
                    p = Popup(self.og_master, "No Trail Selected", "Please select\na trail!")
                    p.wait_window()
                return False
        else:
            for i in range(self.graphDescription["numConfigurations"]):
                trail_name, county, state = split_trail_entry(self.graphDescription["trailConfigs"][i])
                if trail_name is None:
                    p = Popup(self.og_master, "No Trail Selected", "Please select\na trail for\neach configuration!")
                    p.wait_window()
                    return False
        return True


    def clear_graph(self):
        self.ax.clear()
        self.ax.set_title("Set The Fields Above And Click Build Graph In Options!", fontsize=13, color=self.fontColor)
        self.ax.set_xlabel("Timeframe", color=self.fontColor)
        self.ax.set_ylabel("Number of Users", color=self.fontColor)
        self.data = None
        self.graphTitle = ""
        self.canvas.draw()


    def split_query(self):
        self.xValues = []
        self.yValues = []
        for config in self.data:
            self.xValues.append([])
            self.yValues.append([])
            for x, y in config:
                self.xValues[-1].append(x)
                self.yValues[-1].append(y)


    def set_dark_mode(self):
        self.ax.set_facecolor('#2e2e2e')
        self.ax.tick_params(colors=self.fontColor)
        self.ax.xaxis.label.set_color(self.fontColor)
        self.ax.yaxis.label.set_color(self.fontColor)
        self.ax.title.set_color(self.fontColor)
        self.canvas.draw()


    def build_graph(self, popup=True):
        def switch_date_order(date: str):
            date += "-"
            date += date[:4]
            return date[5:]
        self.clear_graph()
        if not self.validate_query(popup=popup):
            return
        self.choose_query()
        self.split_query()
        self.ax.clear()
        self.ax.set_title(self.graphTitle, fontsize=13, color=self.fontColor)
        for i, config in enumerate(self.data):
            if self.graphDescription["cmpTrailsOrDates"] == 1:
                legendLabel = switch_date_order(self.dateConfigs[i][0]) + ' to ' + switch_date_order(self.dateConfigs[i][1])
            else:
                trail, _, _ = self.trailConfigs[i]
                legendLabel = trail
            if self.settings.graph_type() == "Line":
                self.ax.plot(self.xValues[i], self.yValues[i], label=legendLabel, color=self.colors[i])
            elif self.settings.graph_type() == "Bar":
                self.ax.bar(self.xValues[i], self.yValues[i], label=legendLabel, color=self.colors[i])
            elif self.settings.graph_type() == "Scatter":
                self.ax.scatter(self.xValues[i], self.yValues[i], label=legendLabel, color=self.colors[i])
        # only plot up to 12 values on the x-axis
        if len(self.xValues[0]) > 12:
            ticks = [self.xValues[0][0]]
            tick_nums = [0]
            for i in range(len(self.xValues[0]) // 12, len(self.xValues[0]), len(self.xValues[0]) // 12):
                ticks.append(self.xValues[0][i])
                tick_nums.append(i)
            self.ax.set_xticks(tick_nums)
            self.ax.set_xticklabels(ticks, color=self.fontColor)
        else:
            self.ax.set_xticks([i for i in range(len(self.xValues[0]))])
            self.ax.set_xticklabels(self.xValues[0], color=self.fontColor)
        if self.settings.grid():
            self.ax.grid(color="gray", linewidth=0.2)

        if self.settings.legend():
            self.ax.legend()
            legend = self.ax.legend()
            for text in legend.get_texts():
                text.set_color(self.fontColor)
            legend.get_frame().set_facecolor('#4e4e4e')
            legend.get_frame().set_edgecolor(self.fontColor)
        if not self.settings.zoom_graph():
            bottom, top = self.ax.get_ylim()
            self.ax.set_ylim(bottom=0, top=top)
        self.canvas.draw()


    def save(self):
        if self.data is None:
            p = Popup(self.og_master, "No Graph", "No graph to\nsave. Please build\na graph first!")
            p.wait_window()
            return
        sanitized_title = sub(r'[\\/*?:"<>|\r]', "_", self.graphTitle).strip()
        sanitized_title = sub(r'\n', " ", sanitized_title).strip()
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                     initialfile= sanitized_title + ".png",
                                     title="Save graph as")
        if file_path:
            self.fig.savefig(file_path)

"""
Example graph description for reference:

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
"""












