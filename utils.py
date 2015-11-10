#!/usr/bin/env python3
# functions.py


def Flight(on, onTime, onPrice, back, backTime, backPrice):
    from collections import OrderedDict
    flight = OrderedDict([
        ('on', on), ('onTime', onTime), ('onPrice', onPrice),
        ('back', back), ('backTime', backTime), ('backPrice', backPrice),
        ('totalPrice', onPrice + backPrice)
    ])
    return flight


def StringsToDates(_list):
    dates = []
    for strDate in _list:
        dates.append(StringToDate(strDate))
    return sorted(dates)


def SortFlightsByDate(_list):
    return sorted(_list, key=lambda d: d['on'])


def SortFlightsByPrice(_list):
    return sorted(_list, key=lambda d: d['onPrice'] + d['backPrice'])


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


def StringToTime(string):
    from datetime import datetime
    return datetime.strptime(string, '%H:%M:%S').time()


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
    ryanairDays = 365
    ryanairDateEnd = date.today() + timedelta(ryanairDays)
    if ryanairDateEnd < date_end:
        date_end = ryanairDateEnd
    days_delta = date_end - date_start
    days = days_delta.days + 1
    dates = []
    for days_to_add in range(days):
        day = date_start + timedelta(days_to_add)
        dates.append(day)
    return dates
