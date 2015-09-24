#!/usr/bin/env python3
# scraper.py

# from argparse import ArgumentParser
#
# parser = ArgumentParser()
# parser.add_argument("get", help="get data")
#
# # args = parser.parse_args()

# line in master only

import logging
logging.basicConfig(level=logging.DEBUG)  # debug or info
log = logging.getLogger(__name__)

if __name__ == '__main__':
    from sys import argv as args
    config_filename = args[1]
    log.debug("config file: %s", config_filename)
    from utils import ReadConfig
    config = ReadConfig(config_filename)
    log.debug("configs: %s", config)
    from utils import GenerateDates
    dates = GenerateDates(config['from_date'], config['to_date'])
    log.debug("dates: %s", len(dates))
    from utils import ReadJson
    db = ReadJson(config['db'])
    log.debug('database: %s', str(db))
    from scraper import Scraper
    with Scraper(dates, config['from'], config['to'], db) as scraper:
        flights = scraper.getFlights()
    from utils import WriteJson
    WriteJson(config['db'], flights)
