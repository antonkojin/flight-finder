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
        print('{:10}\t{:5}\t{:>6}\t{:10}\t{:5}\t{:>6}\t{:>6}'.format(
                'on', 'time', 'price', 'back', 'time', 'price', 'total'
                ))
        f = '{0:10}\t{1:5}\t{2:>6,.2f}\t{3:10}\t{4:5}\t{5:>6,.2f}\t{6:>6,.2f}'
        for flight in weekendFlights:
            print(f.format(
                str(flight['on']),
                str(flight['onTime'])[:-3],
                flight['onPrice'],
                str(flight['back']),
                str(flight['backTime'])[:-3],
                flight['backPrice'],
                flight['totalPrice']
            ))

    def printHistogram(self):
        pass

    def printDateHistogram(self):
        pass
