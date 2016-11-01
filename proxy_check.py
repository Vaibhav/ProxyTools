import urllib2, socket

socket.setdefaulttimeout(180)

# read the list of proxy IPs in proxyList

def is_bad_proxy(pip):    
    try:        
        proxy_handler = urllib2.ProxyHandler({'http': pip})        
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)        
        req=urllib2.Request('http://www.google.com')  # change the url address here
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:        
        print 'Error code: ', e.code
        return e.code
    except Exception, detail:

        print "ERROR:", detail
        return 1
    return 0


filename = "proxylist-2016-11-01-01-32-21.txt"

f = open(filename)
proxyList = [];

for line in f:
	line = line.rstrip('\n')
	proxyList.append(line)
	
print proxyList

x = open("new.txt", 'w')
count = 0

for item in proxyList:
    if is_bad_proxy(item):
		print "Bad Proxy", item
		count = count + 1;
    else:
        x.write(item);
	x.write('\n');

print "SO MANY BAD PROXIES " + str(count)
x.close()
f.close()
