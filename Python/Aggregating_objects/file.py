class File:
    def __init__(self, trail: str, start_date: str, end_date: str, path: str):
        self.path = path
        self.trail = trail
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f"Trail: {self.trail}\
                Start Date: {self.start_date}\
                End Date: {self.end_date}\
                Path: {self.path}"
    def __repr__(self):
        return f"File('{self.trail}', '{self.start_date}', '{self.end_date}', '{self.path}')"