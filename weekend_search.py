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
    for date_str, times_str in on_db.items():
        _date = StringToDate(date_str)
        times = sorted([StringToTime(time_str) for time_str in times_str])
        log.debug("times: " + str(times))
        if _isFriday(_date):

    return weekends
