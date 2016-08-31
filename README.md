# ProxyTools

This repository contians a long python script which scrapes proxies from the top free proxy websites. 

These websites are the ones I acrape the proxies from:
 - http://proxy-list.org/
 - http://us-proxy.org/
 - http://free-proxy-list.net/
 - http://cool-proxy.net/
 - http://samair.ru/
 - http://aliveproxy.com/
 - http://nntime.com/

Soon to come:
 - http://www.proxylisty.com/
 
 
One run usually gets around 3000 fresh proxies. 

The script takes a while to compile the list as it has to retrieve the proxy from each of the websites. 
 
## Bugs

Some of the output contains html tags along with the proxy address. 

The "proxylisty" implementation I currently have, does not work properly. 
 
You have to press enter after it says "Please Wait...". It doesn't automatically save the file, it waits for the user to press enter. 