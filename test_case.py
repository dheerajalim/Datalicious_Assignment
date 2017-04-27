import unittest

from selenium import webdriver

import time
import json
from browsermobproxy import Server
import csv

import parameters


urls = [] # A list to store all URL's in the HAR file
google_analytics_parameters = [] # A list to store all required google analytics parameters e.g dp, dt

parameters_value =[] # This will create a list of all parameter values of google analytics


# Function to create JSON file
def create_json(result):

    # Produces a new file named Datalicious_HAR, which is located in the directory where the script is run from
    file = open(parameters.HAR_JSON_FILE, 'w+')
    file.write(result)  # Writes to Datalicious_HAR.json, appending the earlier variable "result"
    file.close()  # Saves and closes Datalicious_HAR.json

# Function to write CSV file


def create_csv(filename,value):
    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerow(value)
        print("CSV LOG File generated")


class DataliciousRequest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Initiating the Browsermob proxy Server

        cls.server = Server(parameters.BROWSERMOB_SERVER_PATH)
        cls.server.start()
        cls.proxy = cls.server.create_proxy({"port":9911})

        # Creating the test for Chrome

        cls.profile = webdriver.ChromeOptions()
        cls.profile.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=cls.proxy.port))

        cls.driver = webdriver.Chrome(executable_path = parameters.CHROME_EXE_PATH, chrome_options=cls.profile)

        # Setting a new HAR to be recorded

        cls.proxy.new_har("Datalicious")

        # Starting the browser to perform the following tasks
        '''
        Go to google.com
        Select search input
        Put in Datalicious
        Click Search
        Wait till results are shown
        Click first result from organic search
        '''
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
        cls.driver.get(parameters.WEBSITE_URL)
        cls.driver.find_element_by_name("q").send_keys(parameters.WEBSITE_SEARCH_TERM)
        cls.driver.find_element_by_name("q").submit()
        time.sleep(2)

        # Clicking on the first organic search

        cls.driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div/h3/a').click()

    def test01_checking_request(self):

        # creating the json dumps for the har recording
        result = json.dumps(self.proxy.har, ensure_ascii=False)

        # converting the result into string

        result = str(result)

        # Creating a JSON file to store the HAR recording
        create_json(result)

        # This will stop the process running the proxy

        self.server.stop()

        # Parsing the json file to check for the requests
        global google_analytics_parameters
        with open(parameters.HAR_JSON_FILE) as json_data:
            data = json.load(json_data)
            for r in data['log']['entries']:
                urls.append(r['request']['url'])
                if parameters.GOOGLE_ANALYTICS_REQUEST in r['request']['url']:
                    # Check for dt and dp parameters
                    google_analytics_parameters.append(r['request']['queryString'])

        # Now lets check for the required request in generated URLS
        googleanalytics_request = [i for i, s in enumerate(urls) if parameters.GOOGLE_ANALYTICS_REQUEST in s]
        optimahub_request = [i for i, s in enumerate(urls) if parameters.OPTIMAHUB_REQUEST in s]

        if not googleanalytics_request:
            print("Request was not made to Google Analytics")
        else:
            print("Request was made to Google Analyitcs")

        if not optimahub_request:
            print("Request was not made to dc.optimahub.com")
        else:
            print("Request was made to dc.optimahub.com")

    def test02_checking_request_parameters(self):

        # This will check for the parameters in Google Analytics

        flag_dt = 0 # A flag for dt variable
        flag_dp = 0 # A flag for dp variable
        global google_analytics_parameters

        for data in google_analytics_parameters:
            for content in data:
                if content['name'] == parameters.GA_DT_PARA:

                    parameters_value.append("dt = " + content['value'])
                    flag_dt = 1

                if content['name'] == parameters.GA_DP_PARA:

                    parameters_value.append("dp = " + content['value'])
                    flag_dp = 1

        if flag_dt == 0:
            parameters_value.append("dt = parameter unavailable")

        if flag_dp == 0:
            parameters_value.append("dp = parameter unavailable")

        create_csv(parameters.CSV_FILE_NAME,parameters_value)

    @classmethod
    def tearDownClass(cls):

        cls.driver.quit()
        print("Test Completion")


if __name__ == "__main__":
    unittest.main(verbosity=2)












