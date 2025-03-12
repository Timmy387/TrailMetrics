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


