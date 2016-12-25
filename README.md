# ProxyTools

This repository contians a long python script which scrapes proxies from the top free proxy websites. 

These websites are the ones I scrape the proxies from:
 - http://proxy-list.org/
 - http://us-proxy.org/
 - http://free-proxy-list.net/
 - http://cool-proxy.net/
 - http://samair.ru/
 - http://aliveproxy.com/
 - http://nntime.com/

Soon to come:
 - Proxy Checker, check if the proxies are working and delete proxies that do not. Thus, shortening thel ist of proxies    to include only the best of the best.  
 
One run usually gets around 3000+ fresh proxies. 

The script takes a while to compile the list as it has to retrieve the proxy from each of the websites. 

How to run the script:

```python
python proxy-scraper.py
```

 
## Bugs


The "proxylisty" implementation I currently have, does not work properly. When scraping ProxyListy it keeps outputting "not a gzipped file".  
 
You have to press enter after it says "Please Wait...". It doesn't automatically save the file, it waits for the user to press enter. ---> Somewhat FIXED


### Fixed

FIXED: Some of the output contained HTML tags with the proxy addresses embedded within the tags. Used regex to remove the tags. 


FIXED: Missing port numbers for some of the proxies due to proxy addresses and ports being in different parts of the document object model. 

#### License


MIT

**Free Software, Hell Yeah!**
