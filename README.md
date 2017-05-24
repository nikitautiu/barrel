# barrel
General purpose email/keyword regex crawler for non-illicit purposes.


## How to run
Simply install the requirements. The project adds a new scrapy command `barrel` which can be used to perform broad crawls. 
It takes the same options as `scarpy crawl`, but adds a couple additional arguments. 

To do a run:
* Install the requirements
* Create a `local_settings.py` file at the root of the project to override the default keywords.
```python
from barrel.settings.settings import *

# this checks if the letters a and b appear on the page
KEYWORD_ITEMS = {
    'a': r'a',
    'b': r'b'
}

# this collects all numbers inside paragraphs
COLLECT_ITEMS = {
    'numbers': {'regex': r'[0-9]+', 'css': 'p'} 
```
For more info on the syntax, check `barrel.extractor`

* Run with these settings:
```bash
SCRAPY_SETTINGS_MODULE=local_settings scrapy barrel http://someurl.com/
```

**Note:** All settings can be overriden with the `-s` option just la `scarpy crawl`
