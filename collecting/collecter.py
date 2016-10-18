from BeautifulSoup import BeautifulSoup
import urllib2, urllib, threading, sys

url = "http://apk.hiapk.com/apps"
down_url = "http://apk.hiapk.com/appdown/"
info_url = "http://apk.hiapk.com/appinfo/"
num = 11
page = 5

def makelist(n):
    f = open('url{:02d}.txt'.format(n), 'w')
    for i in range((n-1) * page, n * page):
        if i == 0:
            continue
        print '[!] start page %s' %i
        data = urllib.urlencode({'pi': i})
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response)

        for link in soup.find("div", {"id": "softListBox"}).findAll("a"):
            href = link.get('href')
            if "appdown" in str(href):
                u = href.replace('/appdown/','')
                s = BeautifulSoup(urllib2.urlopen(info_url + u, timeout=1000))
                tmp = s.find('div', {"id": "otherSoftBox"}).findAll('dt', {"class": "font14"})
                print "[+] %s" %u
                for l in tmp:
                    print "[!] %s:%s" % (l.find('a').get('href'), l.find('a').contents[0])
                    f.write(l.find('a').get('href').replace('/appinfo/','') + ":" + l.find('a').contents[0] + ":" + u + '\n')


    f.close()


threads = []
for mon in xrange(1, num):
    print '[+] Thread %d is start' %mon
    t = threading.Thread(target=makelist, args=(mon,))
    threads.append(t)
    t.start()


for t in threads:
    t.join()
