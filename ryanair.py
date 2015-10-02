#!/usr/bin/env python3
# scraper.py

import logging
# logging.basicConfig(level=logging.INFO)  # debug or info
# logging.basicConfig(level=logging.DEBUG)  # debug or info
log = logging.getLogger(__name__)


def parseArgs():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-p", "--parse", action="store_true")
    parser.add_argument("-w", "--weekends", action="store_true")
    parser.add_argument("config_file")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()
    log.debug(args)
    if not args.parse and not args.weekends:
        parser.error("at least one of --parse or --weekends is required")
    return args


def runParse(config):
    from scraper import Scraper
    with Scraper(config) as scraper:
        flights = scraper.getFlights()
    from utils import WriteJson
    WriteJson(config['db'], flights)


def runWeekends(config):
    from viewer import Viewer
    view = Viewer(config)
    view.printWeekendFlightsByPrice()


def run(args):
    config_filename = args.config_file
    log.debug("config file: %s", config_filename)
    from utils import ReadConfig
    config = ReadConfig(config_filename)
    log.debug("configs: %s", config)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    if args.parse:
        runParse(config)
    if args.weekends:
        runWeekends(config)


if __name__ == "__main__":
    args = parseArgs()
    run(args)
