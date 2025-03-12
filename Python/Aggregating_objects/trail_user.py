class TrailUser:
    def __init__(self, date: str, time: str, location: str, group_size: int):
        self.date = date
        self.time = time
        self.location = location
        self.group_size = group_size

    def __str__(self):
        return f"Date: {self.date}\
                Time: {self.time}\
                Location: {self.location}\
                Group Size: {self.group_size}"

    def __repr__(self):
        return f"Trail User('{self.date}', '{self.time}', '{self.location}', '{self.group_size}')"