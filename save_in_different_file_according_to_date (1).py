#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 08:43:52 2017

@author: amitbansal
"""
import os
import re
import time

start_time = time.clock()

list = ['may','june','july','august','aug','september','sept','october','oct','november','nov','dec','december']
path0 = '/Users/amitbansal/Desktop/test'
path = '/Users/amitbansal/Desktop/result'
for filename in os.listdir(path0):
    b = open(os.path.join(path0,filename),'r')
    c = b.readlines()
    for lines in c: 
        d = lines.split(',')
        for i in range(0,len(d)):
            if (d[i].startswith( 'Status' ) or d[i].startswith( 'retweetedStatus' )):
                e = d[i].split()
                for j in range(0,len(e)):
                    if (e[j].lower() in list):
                        if (str(e[j].lower()) == "july"):
                            if (int(e[j+1])>=1 and int(e[j+1])<=17):
                                dat = str("before_convection")+".txt" 
                                print(dat)
                            elif (int(e[j+1])>=18 and int(e[j+1])<28):
                                dat = str("during_convection")+".txt"
                                print(dat)
                            elif (int(e[j+1])>=29 and e[j+1]<=31):
                                dat = str("after_convection")+".txt"
                                print(dat)
                        else :
                            dat = str(e[j].lower()) + ".txt"
                            print(dat)
                        if (os.path.isfile(os.path.join(path,dat))):
                            f=open(os.path.join(path,dat),'a')
                            for result in re.findall(' text=\'(.*?)\',', lines, re.S):   
                                f.write(result)
                                f.write('\n')
                        else:
                            f=open(os.path.join(path,dat),'w')
                            for result in re.findall(' text=\'(.*?)\',', lines, re.S):    
                                f.write(result)
                                f.write('\n')
                    else:
                        continue
                    
print time.clock() - start_time, "seconds"