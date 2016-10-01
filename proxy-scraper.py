####### ##########
####### #######
'''
   Date: August 2016
   Script downloads the best HTTP proxies from free proxy websites
   Saves a txt file with 1 proxy per line
   This list can easily be used with other bots/programs
'''
####### #######
####### ##########
import time
import datetime
import urllib, urllib2
import threading
import Queue
import re
import StringIO
import gzip
import sys
import socket

socket.setdefaulttimeout(90)
# Reference https://love-python.blogspot.ca/2008/07/check-status-proxy-address.html
def is_bad_proxy(currentProxy):    
    try:
        proxy_handler = urllib2.ProxyHandler({'http': currentProxy})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)
        req = urllib2.Request('http://www.example.com')  # change the URL to test here
        sock = urllib2.urlopen(req)

    except urllib2.HTTPError, e:
        print 'Error code: ', e.code
        return e.code

    except Exception, detail:
        print "ERROR:", detail
        return True
		
    return False


def remove_tags(text):
	"""Remove html tags from a string"""
	clean = re.compile('<.*?>')
	return re.sub(clean, '', text)

def queueThread():
	global proxyCount
	ts = time.time()
	thedate = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
	print ("Saving to proxylist-" + thedate + ".txt")
	fout = open("proxylist-" + thedate + ".txt", "w")
	while not workerQueue.empty():
		line = remove_tags(workerQueue.get())
		# if the port number is missing for the proxy
		# add port 8080 as temporary port
		# since it is the most popular port. 
		if line.endswith(':'):
			line += '8080'
		fout.write(line + "\n")
		proxyCount+=1
	fout.close()


def usproxy():
	print "Grabbing: http://www.us-proxy.org/"
	templs = []
	url = "http://www.us-proxy.org/"
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('Host', 'www.proxylisty.com'),
							('Connection', 'keep-alive'),
							('Cache-Control', 'max-age=0'),
							('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
							('Upgrade-Insecure-Requests', '1'),
							('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'),
							('Referer', 'https://www.google.co.za/'),
							('Accept-Encoding','gzip, deflate, sdch'),
							('Accept-Language','en-US,en;q=0.8')]

		response = opener.open(url, timeout=10)
		html = response.read()

		templs = re.findall(r'<tr><td>(.*?)</td><td>', html)
		templs2 = re.findall(r'</td><td>[1-99999].*?</td><td>', html)

		for i in range(len(templs)):
			temp = templs[i] + ":" + templs2[i].replace('</td><td>', '')
			workerQueue.put(temp)
			# ("usproxy() " + templs[i] + ":" + templs2[i].replace('</td><td>', ''))

	except Exception, e:
		if e.message == " ":
			print ''
		else:
			print e.message
			print "Failed to grab " + "'" + url + "'"



def proxylist():
	print "Grabbing: http://proxy-list.org/"
	primary_url = "http://proxy-list.org/english/index.php?p="
	urls = []
	for i in range(1, 11):
		urls.append(primary_url + str(i))

	for url in urls:
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('Host', 'www.proxylisty.com'),
								 ('Connection', 'keep-alive'),
								 ('Cache-Control', 'max-age=0'),
								 ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
								 ('Upgrade-Insecure-Requests', '1'),
								 ('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'),
								 ('Referer', 'https://www.google.co.za/'),
								 ('Accept-Encoding','gzip, deflate, sdch'),
								 ('Accept-Language','en-US,en;q=0.8')]

			response = opener.open(url, timeout=10)
			compressedFile = StringIO.StringIO()
			compressedFile.write(response.read())
			compressedFile.seek(0)
			decompessedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
			html = decompessedFile.read()

			templs = re.findall(r'<li class="proxy">([1-99999].*)?</li>', html)
			for line in templs:
				workerQueue.put(line)


		except Exception, e:
			if e.message == " ":
				print ''
			else:
				print e.message
				print "Failed to grab " + "'" + url + "'"




def coolproxy():
	print "Grabbing: http://www.cool-proxy.net/"
	primary_url = "http://www.cool-proxy.net/proxies/http_proxy_list/sort:score/direction:desc/page:"
	urls = []
	for i in range(1, 13):
		urls.append(primary_url + str(i))

	for url in urls:
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('Host', 'www.proxylisty.com'),
								 ('Connection', 'keep-alive'),
								 ('Cache-Control', 'max-age=0'),
								 ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
								 ('Upgrade-Insecure-Requests', '1'),
								 ('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'),
								 ('Referer', 'https://www.google.co.za/'),
								 ('Accept-Encoding','gzip, deflate, sdch'),
								 ('Accept-Language','en-US,en;q=0.8')]

			response = opener.open(url, timeout=10)
			compressedFile = StringIO.StringIO()
			compressedFile.write(response.read())
			compressedFile.seek(0)
			decompessedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
			html = decompessedFile.read()

			templs = re.findall(r'str_rot13(.*?)</script>', html)
			templs2 = re.findall(r'<td>[1-99999].*?</td>', html)

			for i in range(len(templs)):
				temp = templs[i].replace('("', '')#remove front of string
				temp = temp.replace('")))', '')#remove back of string
				temp = temp.decode('rot13').decode('base64')#decode from rot13 then from base64
				workerQueue.put(temp + templs2[i].replace('<td>', ':').replace('</td>', ''))
				# bug("coolproxy() " + temp + templs2[i].replace('<td>', ':').replace('</td>', ''))

		except Exception, e:
			if e.message == " ":
				print ''
			else:
				print e.message
				print "Failed to grab " + "'" + url + "'"



def freeproxylist():
	print "Grabbing: http://free-proxy-list.net/"
	url = "http://free-proxy-list.net/"
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('Host', 'www.proxylisty.com'),
							('Connection', 'keep-alive'),
							('Cache-Control', 'max-age=0'),
							('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
							('Upgrade-Insecure-Requests', '1'),
							('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'),
							('Referer', 'https://www.google.co.za/'),
							('Accept-Encoding','gzip, deflate, sdch'),
							('Accept-Language','en-US,en;q=0.8')]

		response = opener.open(url, timeout=10)
		html = response.read()

		templs = re.findall(r'<tr><td>(.*?)</td><td>', html)
		templs2 = re.findall(r'</td><td>[1-99999].*?</td><td>', html)

		for i in range(len(templs)):
			workerQueue.put(templs[i] + ":" + templs2[i].replace('</td><td>', ''))
			# bug("freeproxylist() " + templs[i] + ":" + templs2[i].replace('</td><td>', ''))

	except Exception, e:
		if e.message == " ":
			print ''
		else:
			print e.message
			print "Failed to grab " + "'" + url + "'"



def samair():
	print "Grabbing: http://www.samair.ru/"
	primary_url = "http://www.samair.ru/proxy/proxy-00.htm"
	urls = []

	for i in range(1, 31):
		if i < 10:
			urls.append(primary_url.replace("00", "0" + str(i)))
		else:
			urls.append(primary_url.replace("00", str(i)))

	for url in urls:
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('Host', 'www.proxylisty.com'),
								 ('Connection', 'keep-alive'),
								 ('Cache-Control', 'max-age=0'),
								 ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
								 ('Upgrade-Insecure-Requests', '1'),
								 ('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'),
								 ('Referer', 'https://www.google.co.za/'),
								 ('Accept-Encoding','gzip, deflate, sdch'),
								 ('Accept-Language','en-US,en;q=0.8')]

			response = opener.open(url, timeout=10)
			compressedFile = StringIO.StringIO()
			compressedFile.write(response.read())
			compressedFile.seek(0)
			decompessedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
			html = decompessedFile.read()

			links = re.findall(r'<tr><td>(.*?):(.*?)</td><td>', html)
			for link in links:
				workerQueue.put(link[0] + ":" + link[1])
				# bug("samair() " + link[0] + ":" + link[1])

		except Exception, e:
			if e.message == " ":
				print ''
			else:
				print e.message
				print "Failed to grab " + "'" + url + "'"


def proxylisty():
	print "Grabbing: http://www.proxylisty.com/"
	primary_url = "http://www.proxylisty.com/ip-proxylist-"
	urls = []
	for i in range(1, 68):
		urls.append(primary_url + str(i))

	for url in urls:
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('Host', 'www.proxylisty.com'),
								 ('Connection', 'keep-alive'),
								 ('Cache-Control', 'max-age=0'),
								 ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
								 ('Upgrade-Insecure-Requests', '1'),
								 ('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'),
								 ('Referer', 'https://www.google.co.za/'),
								 ('Accept-Encoding','gzip, deflate, sdch'),
								 ('Accept-Language','en-US,en;q=0.8')]

			response = opener.open(url, timeout=10)
			compressedFile = StringIO.StringIO()
			compressedFile.write(response.read())
			compressedFile.seek(0)
			decompessedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
			html = decompessedFile.read()

			templs = re.findall(r'<tr>\n<td>(.*?)</td>', html)
			templs2 = re.findall(r'com/port/(.*?)-ip-list', html)

			for i in range(len(templs)):
				workerQueue.put(templs[i] + ":" + templs2[i])
				# bug("proxylisty() " + templs[i] + ":" + templs2[i])

		except Exception, e:
			if e.message == " ":
				print ''
			else:
				print e.message
				print "Failed to grab " + "'" + url + "'"

def nntime():
	print "\nGrabbing: http://nntime.com/"
	primary_url = "http://nntime.com/proxy-list-00.htm"
	urls = []
	for i in range(1, 31):
		if i < 10:
			urls.append(primary_url.replace("00", "0" + str(i)))
		else:
			urls.append(primary_url.replace("00", str(i)))

	for url in urls:
		try:
			response = urllib.urlopen(url)
			html = response.read()

			decoder_string = re.findall(r'<script type="text/javascript">\n(.*?)</script>', html)
			decoderls = decoder_string[0].split(";")

			temp_tuple = []
			for itm in decoderls:
				if itm:
					temp_tuple.append((itm.split("=")))

			decoder_dict = dict(temp_tuple)

			ips = re.findall(r'></td><td>(.*?)<script type="text/javascript">document', html)

			ports = []
			templs = re.findall(r'<script type="text/javascript">.*?</script>', html)
			for line in templs:
				temp = line.replace('<script type="text/javascript">document.write(":"+', '')
				temp = temp.replace(')</script>', '')
				codes = temp.split("+")

				temp_port = ""
				for code in codes:
					temp_port += decoder_dict[code]
				ports.append(temp_port)


			for i in range(len(ips)):
				#print ips[i] + ":" + ports[i]
				workerQueue.put(ips[i] + ":" + ports[i])

		except Exception, e:
			if e.message == " ":
				print ''
			else:
				print e.message
				print "Failed to grab " + "'" + url + "'"

def aliveproxy():
	print "\nGrabbing: http://www.aliveproxy.com/"
	urls = []

	url = "http://www.aliveproxy.com/"
	response = urllib.urlopen(url)
	html = response.read()
	pos = html.find("Socks 5")
	html = html[:pos]

	temp_urls = re.findall(r'href=[\'"]?([^\'" >]+)', html)
	for itm in temp_urls:
		if "http://www.aliveproxy.com/proxy-list/proxies.aspx/" in itm:
			urls.append(itm)

	for url in urls:
		response = urllib.urlopen(url)
		html = response.read()
		templs = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})', html)
		for itm in templs:
			workerQueue.put(itm[0] + ":" + itm[1])


#============================================================================================


if __name__ == "__main__":

	print "==========================="
	print "Starting Proxy Scraper..."
	print "==========================="
	proxyCount = 0

	workerQueue = Queue.Queue()

	pQueueThread = threading.Thread(target=queueThread)
	pQueueThread.setDaemon(True)

	pProxylist = threading.Thread(target=proxylist)
	pProxylist.setDaemon(True)

	pUsproxy = threading.Thread(target=usproxy)
	pUsproxy.setDaemon(True)

	pFreeproxylist = threading.Thread(target=freeproxylist)
	pFreeproxylist.setDaemon(True)

	pCoolproxy = threading.Thread(target=coolproxy)
	pCoolproxy.setDaemon(True)

	pSamair = threading.Thread(target=samair)
	pSamair.setDaemon(True)

	#pProxylisty = threading.Thread(target=proxylisty)
	#pProxylisty.setDaemon(True)

	pAliveproxy = threading.Thread(target=aliveproxy)
	pAliveproxy.setDaemon(True)

	pNntime = threading.Thread(target=nntime)
	pNntime.setDaemon(True)

	print "All threads set, starting threads..."

	pProxylist.start()

	time.sleep(2)

	pUsproxy.start()

	time.sleep(2)

	pFreeproxylist.start()

	time.sleep(2)

	pCoolproxy.start()

	time.sleep(2)

	pSamair.start()

	time.sleep(2)

	#pProxylisty.start()
	#time.sleep(2)

	pAliveproxy.start()

	pNntime.start()

	time.sleep(2)

	print "Fetching data..."
	print "\nPlease wait..."
	print "\nIf it takes too long, try pressing enter, it may trigger the program to finish."

	pProxylist.join()
	pUsproxy.join()
	pFreeproxylist.join()
	pCoolproxy.join()
	pSamair.join()
	#pProxylist.join()
	pAliveproxy.join()
	pNntime.join()


	if not workerQueue.empty():
		pQueueThread.start()
		pQueueThread.join()
		print "Saved to file!\n"
		print "Proxies found: " + str(proxyCount)
	else:
		print "Could not scrape any proxies!"


	raw_input("\nPress any key to exit...")

	sys.exit()

print "Finish!"
