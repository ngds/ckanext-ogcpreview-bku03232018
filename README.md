ckanext-ogcpreview
==================

## Run Tests
### Step 1
Before running tests, there are 2 configs files for test, need to be configured regarding the test environment of your machine:
- ckanext-ogcpreview/test.ini: overrides ckan environment.ini variables or you can point it into a different environment.ini
- ckanext-ogcpreview/ckanext/ogcpreview/tests/tests_config.cfg:
ckan_web_map_service_url: by default it's webMapService (WmsServer service).

### Step 2
Command line to perform the tests:

```
$ cd ckanext-ogcpreview/ckanext/ogcpreview
$ nosetests --ckan --with-pylons=../../test.ini tests/
```
- --with-pylons it's an option to specify the path to environment.ini to use for the test (override ckan default ini).
- tests/ it's the path to all tests files where located
