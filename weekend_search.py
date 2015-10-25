#!/usr/bin/env python3
# weekend_search.py

import logging
log = logging.getLogger(__name__)


def _isFriday(_date):
    isFriday = _date.isoweekday() == 5
    return isFriday


def _nextSunday(_date):
    from datetime import timedelta
    days = 7 - _date.isoweekday()
    daysDelta = timedelta(days)
    sunday = _date + daysDelta
    return sunday


def WeekendSearch(db):
    weekends = []
    on_db = db['on']
    back_db = db['back']
    from utils import StringToDate, StringToTime
    for date_str in on_db:
        _date = StringToDate(date_str)
        if _isFriday(_date):
            friday = _date
            sunday = _nextSunday(friday)
            if str(sunday) in back_db:
                timesFriday = sorted(list(on_db[str(friday)].keys()))
                lastTimeFriday = StringToTime(timesFriday[-1])
                checksLastTimeFriday = sorted(list(on_db[str(friday)][str(lastTimeFriday)].keys()))
                lastCheckLastTimeFridayStr = checksLastTimeFriday[-1]
                priceLastCheckLastTimeFriday = float(on_db[str(friday)][str(lastTimeFriday)][lastCheckLastTimeFridayStr])
                timesSunday = sorted(list(back_db[str(sunday)].keys()))
                lastTimeSunday = StringToTime(timesSunday[-1])
                # checksLastTimeSunday = sorted(list(back_db[str(sunday)][str(lastTimeSunday)].keys()))
                # lastCheckLastTimeSundayStr = checksLastTimeSunday[-1]
                priceLastCheckLastTimeSunday = float(on_db[str(friday)][str(lastTimeFriday)][lastCheckLastTimeFridayStr])
                totalPrice = priceLastCheckLastTimeFriday + priceLastCheckLastTimeSunday
                from collections import OrderedDict
                flight = OrderedDict([
                    ('on', friday), ('onTime', lastTimeFriday), ('onPrice', priceLastCheckLastTimeFriday),
                    ('back', sunday), ('backTime', lastTimeSunday), ('backPrice', priceLastCheckLastTimeSunday),
                    ('totalPrice', totalPrice)
                ])
                log.debug(flight)
                weekends.append(flight)
    return weekends
