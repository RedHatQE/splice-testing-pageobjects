import unittest

class WebuiTestCase(unittest.TestCase):
    def assertElementValue(self, element, value):
        '''assert an WebUI element get_attribute('value') equals value'''
        self.assertEqual(element.get_attribute('value'), value)
