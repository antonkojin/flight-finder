#!/usr/bin/env python3
# weekend_search.py

import logging
log = logging.getLogger(__name__)

def _isFriday(_date):
    return True

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
            pass
    return weekends
