import unittest
import logging
import socket
imiport datetime as dt
import configparser
from pathlib import Path

class test_case(unittest.TestCase):
    """Parent class for all test case in framework."""
    @classmethod
    def setUpClass(self):
        try:
            Path.mkdir(Path("Logs", dt.datetime.now().strftime("%m_%d_%y")), parents=True)
            self.LOG_DIR = Path("Logs", dt.datetime.now().strftime("%m_%d_%y"))
        except FileExistsError:
            self.LOG_DIR = Path("Logs", dt.datetime.now().strftime("%m_%d_%y"))

        #setting up logger
        #Log file string for passing to logging config
        self.LOG_FILE = str(Path(self.LOG_DIR, dt.datetime.now().strftime("%m-%d-%y %I_%M_%S") + "_" +str(__class__.name__) + ".log").absolute())
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename=self.LOG_FILE level=logging.INFO, format=LOG_FORMAT, filemode='a')
        self.logger = logging.getLogger("unittestLogger")
        self.logger.info("Running " + str(__class__.__name__))
        
        #getting vars from config
        config = configparser.ConfigParser()
        config.read("config.ini")
        #Reporting test vars
        self.applciation_id = config.get('REPORTING', 'application_id')
        #API Vars
        self.api_user = config.get('TEST_API', 'PASSWD')
        #Put env check here
        if self.HOSTNAME == "computer name here":
            self.sender_email = config.get('EMAIL', 'sender_email')
        else:
            self.sender_email = config.get('EMAIL', 'sender_email')
            
        #dictionary with test case id/result key value pair
        self.test_cases = {}
    @classmethod
    def tearDownClass
        #shutting down logging
        logging.shutdown()
        print("Sending " + self.LOG_FILE)