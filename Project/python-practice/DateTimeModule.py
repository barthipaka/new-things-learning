import datetime


def get_current_datetime():
    """Returns the current date and time."""
    ref=datetime.datetime.now()
    print(f"Current date and time: {ref}")
    print(f"Current year: {ref.year}")
    print(f"Current year: {ref.max.year}")
    print(f"Current time: {ref.strftime('%H:%M:%S')}")

get_current_datetime()
