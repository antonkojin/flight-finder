#!/usr/bin/env python3
# scraper.py

import logging
log = logging.getLogger(__name__)


class Scraper:
    def __init__(self, config):
        self.config = config
        from utils import ReadJson
        self.flights = ReadJson(self.config['db'])
        log.debug('database: %s', str(self.flights))
        self.timeout = 5
        from utils import GenerateDates
        self.dates = GenerateDates(self.config['from_date'], self.config['to_date'])
        log.debug("dates: %s", len(self.dates))
        self.fromAirport = self.config['from']
        self.toAirport = self.config['to']
        self.baseUrl = 'https://www.bookryanair.com/SkySales/Booking.aspx?culture=en-GB&lc=en-GB#Search'
        log.debug('scraper: %s', str(self))
        from selenium import webdriver
        self.webdriver = webdriver.PhantomJS()
        log.debug('webdriver opened')

    def parse(self, _date):
        self.webdriver.get(self.baseUrl)
        self.__select_twoway()
        self.__select_origin()
        self.__select_destination()
        self.__select_date(_date)
        self.__submit_search()
        self.__ok_same_date()
        log.debug("%s: form filled", str(_date))
        """ go flights """
        flights_xpath = '//*[@id="main"]/article[2]/div[1]/table/tbody'
        self.waitFor(flights_xpath)
        self.webdriver.save_screenshot('out.png')
        flights_xpath += '/tr'
        flights = self.webdriver.find_elements_by_xpath(flights_xpath)
        log.debug('%s: flights: %s', str(_date), len(flights))
        for i in range(1, len(flights) + 1):
            flight_xpath = flights_xpath + '[' + str(i) + ']'
            time_xpath = flight_xpath + '/td[2]'
            time_text = self.webdriver.find_element_by_xpath(time_xpath).text
            from datetime import datetime, time
            _time = time(int(time_text[:2]), int(time_text[3:5]))
            _datetime = datetime.combine(_date, _time)
            log.debug('datetime: %s', str(_datetime))
            price_xpath = flight_xpath + '/td[4]/span'
            price = float(self.webdriver.find_element_by_xpath(price_xpath).text)
            log.debug('%s: %s', str(_datetime), str(price))
            self._add_db(_datetime, price, isReturn=False)

        flights_xpath = '//*[@id="main"]/article[3]/div[1]/table/tbody'
        self.waitFor(flights_xpath)
        flights_xpath = flights_xpath + '/tr'
        flights = self.webdriver.find_elements_by_xpath(flights_xpath)
        log.debug('%s: flights: %s', str(_date), len(flights))
        for i in range(1, len(flights) + 1):
            flight_xpath = flights_xpath + '[' + str(i) + ']'
            time_xpath = flight_xpath + '/td[2]'
            time_text = self.webdriver.find_element_by_xpath(time_xpath).text
            from datetime import datetime, time
            _time = time(int(time_text[:2]), int(time_text[3:5]))
            _datetime = datetime.combine(_date, _time)
            log.debug('datetime: %s', str(_datetime))
            price_xpath = flight_xpath + '/td[4]/span'
            price = float(self.webdriver.find_element_by_xpath(price_xpath).text)
            log.debug('%s: %s', str(_datetime), str(price))
            self._add_db(_datetime, price, isReturn=True)

    def _add_db(self, _datetime, price, isReturn=False):
        if isReturn:
            db = self.flights['back']
        else:
            db = self.flights['on']
        if str(_datetime.date()) not in db:
            db[str(_datetime.date())] = {}
        from datetime import datetime
        if str(_datetime.time()) not in db[str(_datetime.date())]:
            db[str(_datetime.date())][str(_datetime.time())] = {}
        db[str(_datetime.date())][str(_datetime.time())][str(datetime.today())] = price

    def getFlights(self):
        for date in self.dates:
            log.info("parsing date: {}".format(date))
            from selenium.common.exceptions import TimeoutException
            try:
                self.parse(date)
            except TimeoutException:
                log.debug('##### web driver restarted due to timeout #####')
                self.webdriver.quit()
                from selenium import webdriver
                self.webdriver = webdriver.PhantomJS()
                self.parse(date)
        return self.flights

    def __select_twoway(self):
        """ select one way checkbox """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        wait = WebDriverWait(self.webdriver, self.timeout)
        wait.until(EC.presence_of_element_located((By.ID, "SearchInput_RoundTrip")))
        twoway_form = self.webdriver.find_element_by_id('SearchInput_RoundTrip')
        twoway_form.click()

    def __select_origin(self):
        """ origin airport """
        # from selenium.webdriver.common.by import By
        # from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        # wait = WebDriverWait(self.webdriver, self.timeout)
        # wait.until(EC.presence_of_element_located((By.NAME, 'SearchInput$Orig')))
        from selenium.webdriver.support.ui import Select
        origin_form = Select(self.webdriver.find_element_by_name('SearchInput$Orig'))
        origin_form.select_by_value(self.fromAirport)

    def __select_destination(self):
        """ destination airport """
        from selenium.webdriver.support.ui import Select
        destination_form = Select(self.webdriver.find_element_by_name('SearchInput$Dest'))
        destination_form.select_by_value(self.toAirport)

    def __select_date(self, date):
        """ departure date """
        date_form = self.webdriver.find_element_by_name('SearchInput$DeptDate')
        date_form.clear()
        date_form.send_keys(date.strftime("%d/%m/%Y"))
        date_form = self.webdriver.find_element_by_name('SearchInput$RetDate')
        date_form.clear()
        date_form.send_keys(date.strftime("%d/%m/%Y"))

    def __submit_search(self):
        submit = self.webdriver.find_element_by_id("SearchInput_ButtonSubmit")
        submit.click()

    def __ok_same_date(self):
        xpath = '//*[@id="ng-app"]/div[4]/div/div[3]/button[2]'
        submit = self.webdriver.find_element_by_xpath(xpath)
        submit.click()

    def waitFor(self, xpath):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        wait = WebDriverWait(self.webdriver, self.timeout)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.webdriver.quit()
        log.debug('webdriver closed')

    def __str__(self):
        s = 'dates: '
        for date in self.dates:
            s += str(date)
            s += ', '
        s += 'from: ' + self.fromAirport + ' to: ' + self.toAirport
        return s
