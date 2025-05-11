def dow_number(day):
    day = day.lower()
    match day:
        case "sunday":
            return '0'
        case "monday":
            return '1'
        case "tuesday":
            return '2'
        case "wednesday":
            return '3'
        case "thursday":
            return '4'
        case "friday":
            return '5'
        case "saturday":
            return '6'
    print("Please enter a day of the week.")
    return
    # exit(1)


def split_trail_entry(trail):
    if trail == "Choose":
        return None, None, None
    trail = trail.split(", ")
    trail_name = trail[0]
    county = trail[1]
    state = trail[2]
    return trail_name, county, state