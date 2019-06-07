from datetime import datetime
from datetime  import date
f = open('clean_data4.txt', 'r')
f1 = open('2015-08.txt','a')
f2 = open('2015-09.txt','a')
f3 = open('2015-10.txt','a')
f4 = open('2015-11.txt','a')
f5 = open('2015-12.txt','a')
f6 = open('2016-01.txt','a')
f.readline()

for line in f:
	try:
		arr = line.split("\t",6)
		arr1 = arr[5].split(" ",2)
	
		d = datetime.strptime(arr1[0],"%Y-%m-%d").date()
		
		if (d.year == 2015): 
			if  (d.month == 8):
			
				f1.write(line)
			
			if  (d.month == 9):
			
				f2.write(line)
			
			if  (d.month == 10):
			
				f3.write(line)
				
			if  (d.month == 11):
			
				f4.write(line)
				
			if  (d.month == 12):
			
				f5.write(line)
	    		
	except Exception:
		print "error"
		continue
		
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
	
	
f.close() 