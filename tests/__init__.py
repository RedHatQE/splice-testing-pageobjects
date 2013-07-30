import logging, unittest, yaml, sys, os
from pageobjects import namespace

INVENTORY_FILE='./inventory.yml'
log = logging.getLogger(__name__)

# globals INIT
with open(INVENTORY_FILE) as fd:
    globals().update(namespace.load_ns(yaml.load(fd)))

def skipUnlessHasAttributes(obj, *attributes):
    '''unittest-like skipping decorator'''
    for attribute in attributes:
        if not hasattr(obj, attribute):
            return unittest.skip("{!r} doesn't have {!r}".format(obj, attribute)) 
    return lambda func: func

def setUpPackage():
    '''Set up DISPLAY'''
    try:
        os.environ['DISPLAY'] = ROLES.SELENIUM.display
    except (AttributeError, NameError) as e:
        raise unittest.SkipTest(e.message)

def tearDownPackage():
    pass

