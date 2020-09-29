import sys
import unittest
import logging
import inspect
from random import randint
from test_framework import test_case
from emailResults import send
sys.path.append('/opt/')
#place additional imports below


class first_test_set(test_case):
    """Example of a test set with parent class"""

    @classmethod
    def setUpClass(self):
        """Variables defined in set up will be used throughout the test set class"""
        #calls the setUpClass method of the parent/base class test_case
        super().setUpClass()
        self.logger.info("setting up " + str(__class__.__name__))
        self.num2 = randint(11, 20)
        print("Running " + str(__class__.__name__))

    def setUp(self):
        """Setup method is run individually for each test in the test set"""
        self.ran = randint(21, 30)

    def tearDown(self):
        """Teardown method is run individaully for each test in the test set"""

    def test_random_1_1(self):
        """Example Test 1. Uses assertEqual method to verify equality of two numbers."""
        self.logger.info("Running test: " + str(self._testMethodName))
        self.logger.debug("This number is generated separately for each test: " + str(self.ran))
        self.logger.warning("This is the number used on only the first_set tests " + str(self.num2))
        try:
            self.assertEqual(1, 1)
            self.logger.info(str(self._testMethodName) + " PASSED")
            self.test_cases[str(self._testMethodName)] = ["FAILED", str(self.test_random_1_1.__doc__)]
        except AssertionError:
            self.logger.error(str(self._testMethodName) + " FAILED")
            self.test_cases[str(self._testMethodName)] = ["FAILED", str(self.test_random_1_1.__doc__)]
            self.fail()


    def test_random_1_2(self):
        """Example Test 2. Uses assertTrue method to show inequality of two numbers. This test fails."""
        self.logger.info("Running test: " + str(self._testMethodName))
        #self.logger.info("This number is used on all first_set test using the test_case class: " + str(self.num))
        self.logger.info("This number is generated separately for each test: " + str(self.ran))
        self.logger.info("This is the number used on only the first_set tests " + str(self.num2))
        try:
            self.assertTrue(1 == 2)
            self.logger.info(str(self._testMethodName) + " PASSED")
            self.test_cases[str(self._testMethodName)] = ["FAILED", str(self.test_random_1_2.__doc__)]
        except AssertionError:
            self.logger.error(str(self._testMethodName) + " FAILED")
            self.test_cases[str(self._testMethodName)] = ["FAILED", str(self.test_random_1_2.__doc__)]
            self.fail()


    def test_random_1_3(self):
        """Example Test 3. THis test shows an example of using subtests. A single test can have multiple subtests that can either pass or fail independently. In this case we are checking the range of number 1-6 to see if they are even or odd. If the number is even the test passes"""
        self.logger.info("Running test: " + str(self._testMethodName))
        failure = 0
        for i in range(1, 7):
            with self.subTest(msg="i=" + str(i)):
                try:
                    self.assertEqual(i % 2, 0)
                    self.logger.info(str(self._testMethodName) + " iteration: " + str(i) + " PASSED")
                    self.test_cases[str(self._testMethodName) + "_" + str(i)] = ["PASSED", str(self.test_random_1_3.__doc__)]
                except AssertionError:
                    self.logger.error(str(self._testMethodName) + " iteration: " + str(i) + " FAILED")
                    self.test_cases[str(self._testMethodName) + "_" + str(i)] = ["FAILED", str(self.test_random_1_3.__doc__)]
                    failure = 1
        if failure == 1:
            self.logger.error(str(self._testMethodName) + " FAILED")
            self.test_cases[str(self._testMethodName)] = ["FAILED", str(self.test_random_1_3.__doc__)]
            self.fail()


    def test_random_1_4(self):
        """Example Test 4. This test shows an example of the assertIsNot method."""
        try:
            self.assertIsNot(1, 2)
            self.logger.info(str(self._testMethodName) + " PASSED")
            self.test_cases[str(self._testMethodName)] = ["PASSED", str(self.test_random_1_4.__doc__)]
        except AssertionError:
            self.logger.error(str(self._testMethodName) + " FAILED")
            self.test_cases[str(self._testMethodName)] = ["FAILED", str(self.test_random_1_4.__doc__)]


    def test_random_1_5(self):
        """Example test 5 showing use of assertIn method"""
        try:
            self.assertIn(1, [1, 2, 3])
            self.logger.info(str(self._testMethodName) + " PASSED")
            self.test_cases[str(self._testMethodName)] = ["PASSED", str(self.test_random_1_5.__doc__)]
        except AssertionError:
            self.logger.info(str(self._testMethodName) + " FAILED")
            self.test_cases[str(self._testMethodName)] = ["FAILED", str(self.test_random_1_5.__doc__)]


def logResults(result):
    for failure in result.failures:
        print(failure)
    for error in result.errors:
        print(error)
    logger = logging.getLogger("unittestLogger")
    logger.info("Logging Test Results")
    logger.info(result)
    for failure in result.failures:
        logger.info("FAILURE: " + str(result.failures))
    logger.info("ERRORS: " + str(result.errors))


if __name__ == '__main__':

    main = unittest.main(exit=False)
    result = main.result
    logResults(result)
    TEST_CASES = main.module.first_test_set.test_cases
    LOG_DIR = main.module.first_test_set.LOG_DIR
    LOG_FILE = main.module.first_test_set.LOG_FILE
    SENDER_EMAIL = main.module.first_test_set.sender_email
    """Send email with results"""
    send(LOG_FILE, SENDER_EMAIL, TEST_CASES)
