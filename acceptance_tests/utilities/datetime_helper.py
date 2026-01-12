from datetime import datetime


def human_readable_datetime(date_dict, time_dict):
    """
    Converts date and time dictionaries to a human-readable string.
    Example output: 'Saturday 10 January 2026 10:00'
    """
    dt = datetime(
        int(date_dict["year"]),
        int(date_dict["month"]),
        int(date_dict["day"]),
        int(time_dict["hour"]),
        int(time_dict["minute"])
    )
    print("Datetime helper: " + dt.strftime("%A %d %B %Y %H:%M"))
    return dt.strftime("%A %d %B %Y %H:%M")
