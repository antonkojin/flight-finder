#!/usr/bin/env python3
# scraper.py

import logging
logging.basicConfig(level=logging.INFO)  # debug or info
# logging.basicConfig(level=logging.DEBUG)  # debug or info
log = logging.getLogger(__name__)


def parseArgs():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-p", "--parse", action="store_true")
    parser.add_argument("-w", "--weekends", action="store_true")
    parser.add_argument("config_file")
    args = parser.parse_args()
    log.debug(args)
    return args


def run(args):
    config_filename = args.config_file
    log.debug("config file: %s", config_filename)
    from utils import ReadConfig
    config = ReadConfig(config_filename)
    log.debug("configs: %s", config)

#    from utils import ReadJson
#    db = ReadJson(config['db'])
#    log.debug('database: %s', str(db))
#    from weekend_search import WeekendSearch
#    weekend = WeekendSearch(db)

if __name__ == "__main__":
    args = parseArgs()
    run(args)

#     from scraper import Scraper
#     with Scraper(config) as scraper:
#         flights = scraper.getFlights()
#     from utils import WriteJson
#     WriteJson(config['db'], flights)
