#!/usr/bin/env python3
# functions.py

def WriteJson(filename, data):
    import json
    with open(filename, 'w') as f:
        json.dump(data, f,
                  sort_keys=True,
                  indent=2,
                  separators=(",", ": ")
        )

def ReadJson(filename):
    import json
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

def StringToDate(string):
    from datetime import datetime
    return datetime.strptime(string, '%Y-%m-%d').date()
                        
def ReadConfig(filename):
    config = ReadJson(filename)
    config['from_date'] = StringToDate(config['from_date'])
    config['to_date'] = StringToDate(config['to_date'])
    return config

def GenerateDates(date_start, date_end):
    from datetime import date, timedelta
    assert date_start <= date_end, "invalid dates: " + str(date_start) + " " + str(date_end)
    if date_start <= date.today():
        date_start = date.today() + timedelta(1)
    days_delta = date_end - date_start
    days = days_delta.days + 1
    dates = list()
    for days_to_add in range(days):
        day = date_start + timedelta(days_to_add)
        dates.append(day)
    return dates
