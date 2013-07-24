### Splice testing pageobjects
* Bunch of page objects for Splice WebUI automation
* Ispired by the [Pageobject pattern] (http://pragprog.com/magazines/2010-08/page-objects-in-python)


#### usage
See the tests directory for example usage in test case implementation.
To execute test cases:
```
cp tests/inventory.yml ./
# update inventory.yml as needed
nosetests --with-webuiscreenshots --keep-passing-screenshots
```
