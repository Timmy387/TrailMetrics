class Trail:
    def __init__(self, trail_name: str, county: str, state: str):
        self.trail_name = trail_name
        self.county = county
        self.state = state

    def __str__(self):
        return f"Trail Name: {self.trail_name}\
                County: {self.county}\
                State: {self.state}"

    def __repr__(self):
        return f"Trail('{self.trail_name}', '{self.county}', '{self.state}')"