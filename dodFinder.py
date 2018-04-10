from elasticsearch import Elasticsearch
import re
from ipwhois import IPWhois
import pprint
import csv
import urllib2
import time
import simplejson
import os

def elasticQuerySkel():
    es = Elasticsearch('10.10.3.73:9200', request_timeout=2000)
    #res = es.search(index="logstash-firewall-*", body={"query": {"match_all": {}}})
    res = es.search(index="logstash-bluecoat-v4-*", body={"query": {"match": {"categories" : "Military"}}},size=100)
    ipList = []
    print "[*] Querying Elasticsearch for IPs!!! Please wait ..."
    for hit in res['hits']['hits']:
        try:
            #print("%(@timestamp)s %(src_ip)s %(dst_domain)s %(categories)s" % hit["_source"] % hit["_source"] % hit["_source"] % hit["_source"])
            ipAddr = "%(dst_domain)s"  % hit["_source"]
            ipAdd = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", ipAddr)
            if(ipAdd):
                tempIP = ", ".join(ipAdd)
                ipList.append(tempIP)
                print tempIP
        except Exception as ef:
            #print ef
            pass
    return ipList        

def getDetails(ip):
    tmpIp = ip
    es = Elasticsearch('10.10.3.73:9200', request_timeout=2000)
    res = es.search(index="logstash-bluecoat-v4-*", body={"query": {"match": {"dst_ip" : "%s" % tmpIp}}},size=100)
    for hit in res['hits']['hits']:
        timeStamp = "%(@timestamp)s" % hit["_source"]
        source = "%(src_ip)s"  % hit["_source"]
        return source, timeStamp

def whoisFinder(*tmpIpList):
    tmp = []
    tmp = list(tmpIpList)
    proxy = urllib2.ProxyHandler({'http': 'http://kge13202:Pa^^^^word123@10.10.2.141:8080', 'https': 'http://kge13202:Pa^^^word123@10.10.2.141:8080'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    print "[*] Writing the output the file - Script Result.csv"
    with open("Script Result.csv","wb") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Time Stamp', 'Source IP', 'Destination IP Address', 'Org Name', 'Org Country'])
            for i in tmp:
                for j in range(len(i)):
                    ip = i[j]
                    try:
                        req = urllib2.urlopen('http://ip-api.com/json/%s' % ip)
                        infoDict = simplejson.load(req)
                        print "[*] Querying details for ip => %s" % ip
                        source, timeStamp = getDetails(ip)
                        writer.writerow([timeStamp, source, ip, infoDict["isp"], infoDict["country"]])
                        time.sleep(1)
                    except Exception as ex:
                        print ex
    csvfile.close()

if __name__ == "__main__":
    try:
        os.system("rm 'Script Result.csv'")
    except:
        print "[*] No file found. The file will be created after analysis :)"
        pass
    resultipList = []
    resultipList = elasticQuerySkel()
    try:
        whoisFinder(resultipList)
    except Exception as e:
        print "[*] Something happened. Please find the error here %s" % e
        print "[*] Retrying, Kinldy wait ... "
        time.sleep(5)
        whoisFinder(resultipList)
