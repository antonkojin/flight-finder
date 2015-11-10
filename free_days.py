#!/usr/bin/env python3
# weekend_search.py

import logging
log = logging.getLogger(__name__)


class Searcher:
    def __init__(self, config):
        self.config = config
        from utils import StringsToDates
        self.freeDays = StringsToDates(config["free"])
        log.debug("free days: {}".format(self.freeDays))
        from utils import ReadJson
        flights = ReadJson(self.config['db'])
        self.on_db = flights['on']
        self.back_db = flights['back']

    def searchFreeDaysFlights(self):
        pass
