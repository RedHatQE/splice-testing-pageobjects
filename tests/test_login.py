#!/usr/bin/env python
import tests
import sys, unittest, re, time, os.path, logging, nose, selenium, namespace
from pageobjects.login import LoginPageObject, LogoutPageObject, login_ctx
from selenium_wrapper import SE

KATELLO = tests.ROLES.KATELLO

def setUpModule():
    '''Sanity test KATELLO role'''
    try: 
        KATELLO.url, KATELLO.username, KATELLO.password
    except AttributeError as e:
        raise unittest.SkipTest(e.message)


def tearDownModule():
    pass

class LoginTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # reset SE driver 
        SE.reset(url=KATELLO.url)

    def setUp(self):
        SE.get(KATELLO.url)
        self.verificationErrors = []

    def test_1_Login(self):
        lpo = LoginPageObject()
        lpo.username = KATELLO.username
        lpo.password = KATELLO.password
        lpo.submit()

    def test_2_Logout(self):
        lpo = LogoutPageObject()
        lpo.submit()

    def test_3_LoginCtx(self):
        with login_ctx(KATELLO.url, KATELLO.username, KATELLO.password):
            SE.get(KATELLO.url + "/sam")

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    nose.main()
