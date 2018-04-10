import xlrd
import csv
import os
import time
from collections import defaultdict


def open_file(path):
	wb = xlrd.open_workbook(path)
	sh = wb.sheet_by_index(0)
	csv_file = open('file1.csv', 'wb')
	wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
	for rownum in xrange(sh.nrows):
		wr.writerow(sh.row_values(rownum))
	csv_file.close()
def csvParser(csvFile1):
	columns = defaultdict(list)
	with open(csvFile1, 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			for (k,v) in row.items():
				columns[k].append(v)
	i=0
	k=0
	res1=''
	res2=''
	with open('ipUName.yaml', 'a') as f:
		for j in columns['IP Addresses']:
			res1 = str('"'+j+'"'+':'+' '+'"'+columns['User Name'][i]+'"'+'\n')
			if (columns['User Name'][i]):
                                f.write(res1)
                                #print res1.rstrip('\n')
			i=i+1
	f.close()
	with open('ipNbName.yaml', 'a') as y:
		for x in columns['IP Addresses']:
			res2 = str('"'+x+'"'':'+' '+'"'+columns['Netbios Name'][k]+'"'+'\n')
			if (columns['Netbios Name'][k]):
                                y.write(res2)
                                #print res2
			k=k+1
	y.close()
if __name__ == "__main__":
    #path = raw_input("Enter the file of the path : ")
    try:
		os.system('del *.yaml')
    except:
                pass
    try:
                print ("[*] Processing xlsx file ...")
		open_file('sccm.xlsx')
		print ('[*] Creating yaml ...')
		csvParser('file1.csv')
		print ("[*] Cleaning up ...")
		os.system('del *.xlsx')
		os.system('del *.csv')
		time.sleep(2)
		print ("[*] Done ...")
    except Exception as e:
		print "Script didn't run!!! Please contact ah.aletrs@kotak.com for assistance."
		print e
