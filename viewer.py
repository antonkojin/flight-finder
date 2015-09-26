#!/usr/bin/env python3
# viewer.py

import logging
log = logging.getLogger(__name__)

class Viewer:
    def __init__(self, config):
        self.config = config
        from utils import ReadJson
        self.flights = ReadJson(self.config['db'])

    def _searchWeekendFlights(self):
        from weekend_search import WeekendSearch
        from utils import SortFlightsByPrice
        weekendFlights = SortFlightsByPrice(WeekendSearch(self.flights))
        return weekendFlights

    def printWeekendFlightsByPrice(self):
        weekendFlights = self._searchWeekendFlights()
        s = []
        f = '{0:10}\t{1:5}\t{2:>6}\t{3:10}\t{4:5}\t{5:>6}\t{6:>6}'
        s.append(f.format(
            'on',
            'time',
            'price',
            'back',
            'time',
            'price',
            'total'
        ))
        for flight in weekendFlights:
            s.append(f.format(
                str(flight['on']),
                str(flight['onTime'])[:-3],
                str(flight['onPrice']).rjust(6),
                str(flight['back']),
                str(flight['backTime'])[:-3],
                str(flight['backPrice']),
                str(flight['totalPrice'])
            ))
        s = '\n'.join(s)
        print(s)


    def printHistogram(self):
        pass

    def printDateHistogram(self):
        pass
