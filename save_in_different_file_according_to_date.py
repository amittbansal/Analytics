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
z = 0
for filename in os.listdir(path0):
    b = open(os.path.join(path0,filename),'r')
    c = b.readlines()
    for lines in c: 
        d = lines.split(',')
        for i in range(0,len(d)):
           # print (i)
            if (d[i].startswith( 'Status' ) or d[i].startswith( ' retweetedStatus' )):
                e = d[i].split()
                for j in range(0,len(e)):
                    if (e[j].lower() in list):
                        if (str(e[j].lower()) == "july"):
                            if (int(e[j+1])>=1 and int(e[j+1])<=17):
                                dat = str("before_convection")+".txt" 
                            elif (int(e[j+1])>=18 and int(e[j+1])<28):
                                dat = str("during_convection")+".txt"
                            elif (int(e[j+1])>=29 and e[j+1]<=31):
                                dat = str("after_convection")+".txt"
                        else :
                            dat = str(e[j].lower()) + ".txt"
                    else:
                        continue
                f = i+1
                for x in range(f,len(d)):
                    if (d[x].startswith( ' retweetedStatus' )):
                        z = x
                        break
                for x in range(f,z):
                    if (d[x].startswith( ' text' )):
                        m = d[x].replace(" text='","")
                if(os.path.isfile(os.path.join(path,dat))):
                       filec=open(os.path.join(path,dat),'a')
                       filec.write(m)
                       filec.write('\n')
                else:
                       filec=open(os.path.join(path,dat),'w')
                       filec.write(m)
                       filec.write('\n')       
                        
                f = z
                
print time.clock() - start_time, "seconds"