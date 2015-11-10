#!/usr/bin/env python3
# weekend_search.py

import logging
log = logging.getLogger(__name__)


def WeekendSearch(db):
    return test(db)
    # return _WeekendSearch(db)


def test(db):
    weekends = []
    on_db = db['on'].keys()
    back_db = db['back'].keys()
    from utils import StringsToDates
    on_list = StringsToDates(on_db)
    log.debug(on_list)
    back_list = StringsToDates(back_db)
    log.debug(back_list)
    onsAndBacks = [(on, back) for on in on_list for back in back_list if _isBackForOn(on, back)]
    log.debug(onsAndBacks)
    for on, back in onsAndBacks:
        from utils import StringToTime
        timesOn = [StringToTime(time) for time in sorted(list(on_db[str(on)].keys()))]
        if(_isFriday(on)):
            timesOn = timesOn[-1:]
        if(_isSaturday(on)):
            timesOn = timesOn[:-2]
        log.debug(timesOn)

        timesBack = sorted([StringToTime(_time) for _time in list(back_db[str(back)].keys())])

        # from utils import StringToTime
        # lastTimeOn = StringToTime(timesOn[-1])
        # checksLastTimeOn = sorted(list(on_db[str(on)][str(lastTimeOn)].keys()))
        # lastCheckLastTimeOnStr = checksLastTimeOn[-1]
        # priceLastCheckLastTimeOn = float(on_db[str(on)][str(lastTimeOn)][lastCheckLastTimeOnStr])
        # timesBack = sorted(list(back_db[str(back)].keys()))
        # lastTimeBack = StringToTime(timesBack[-1])
        # priceLastCheckLastTimeBack = float(on_db[str(on)][str(lastTimeOn)][lastCheckLastTimeOnStr])
        # totalPrice = priceLastCheckLastTimeOn + priceLastCheckLastTimeBack
        from utils import Flight
        weekends.append(Flight(on, onTime, onPrice, back, backTime, backPrice))
    return weekends


def _isBackForOn(on, back):
    onsAndBacks = (_isFriday(on) or _isSaturday(on)) and _isSunday(back)
    from datetime import timedelta
    isBackForOn = back >= on and back <= on + timedelta(2)
    return onsAndBacks and isBackForOn


def _isFriday(_date):
    isFriday = _date.isoweekday() == 5
    return isFriday


def _isSaturday(_date):
    return _date.isoweekday() == 6


def _isSunday(_date):
        return _date.isoweekday() == 7


def _nextSunday(_date):
    from datetime import timedelta
    days = 7 - _date.isoweekday()
    daysDelta = timedelta(days)
    sunday = _date + daysDelta
    return sunday


def _WeekendSearch(db):
    weekends = []
    on_db = db['on']
    back_db = db['back']
    from utils import StringToDate, StringToTime
    for date_str in on_db:
        _date = StringToDate(date_str)
        if _isFriday(_date):
            on = _date
            sunday = _nextSunday(friday)
            if str(sunday) in back_db:
                timesFriday = sorted(list(on_db[str(friday)].keys()))
                lastTimeFriday = StringToTime(timesFriday[-1])
                checksLastTimeFriday = sorted(list(on_db[str(friday)][str(lastTimeFriday)].keys()))
                lastCheckLastTimeFridayStr = checksLastTimeFriday[-1]
                priceLastCheckLastTimeFriday = float(on_db[str(friday)][str(lastTimeFriday)][lastCheckLastTimeFridayStr])
                timesSunday = sorted(list(back_db[str(sunday)].keys()))
                lastTimeSunday = StringToTime(timesSunday[-1])
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
