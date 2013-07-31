# Page Objects
from selenium_wrapper import SE
from namespace import load_ns
from locator_assembler import locator_assembler
from pkg_resources import resource_filename
import yaml

LOCATORS_FILE="data/locators.yml"
PAGES_FILE="data/pages.yml"

# load&assemble the locators
with open(resource_filename(__name__, LOCATORS_FILE)) as fd:
    locators = load_ns(yaml.load(fd), leaf_processor=lambda x: locator_assembler(x[0], x[1]))

# load the pages
with open(resource_filename(__name__, PAGES_FILE)) as fd:
    pages = load_ns(yaml.load(fd))

