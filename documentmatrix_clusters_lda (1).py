import textmining
import numpy as np
import lda
import peach as p
from numpy import *
from numpy.random import random

fileinput  = open("test.txt").readlines()  # text file as input
fileoutput = open("output.txt", "wb")      # text file where topics were saved

def term_document_matrix():
    num_lines = 0 
    for line in fileinput:
       num_lines = num_lines + 1            #calculate the number of lines a text document
       reading_file_info = [item.rstrip('\n') for item in fileinput]
       tdm = textmining.TermDocumentMatrix()       # creation of the list tdm for document matrix 
       for i in range(0,num_lines): 
           tdm.add_doc(reading_file_info[i])    # Add data to the matrix line by line  tokenize is done by itself
    tdm.write_csv('TermDocumentMatrix.csv',cutoff=1)            # csv document term matrix created by TermDocumentMatrix name 
    temp = list(tdm.rows(cutoff=1))     #temp has all the rows of the document term matrix
    vocab = tuple(temp[0])              # the row which have the each word of the document    
    x=np.array(temp[1:])                # starting from the second row of a matrix as initial is only the words
# cluster creation    
    mu = random((num_lines, 6))        # generate the random number for cluster according to the number of data inserted in document matrix and 3 is the no of clusters should be created which can change
    fcm = p.FuzzyCMeans(x, mu, 2)       # create the clusters 
    num_arra =  fcm.mu
    summation = num_arra.sum(axis = 1)  # calculate the sum of each row of the document matrix as a numpy array
    summation_vertical = summation[:, None] #make the horizontal sum array to vertical array which is easy for furtur access
    rows = num_arra.shape[0]                # give the number of rows of a n-dimension numpy array
    columns = num_arra.shape[1]             # give the number of columns of a n-dimension numpy array
    num_arra=num_arra.astype(float)         # change the int array to float to store the float value 
    for rows_count in range (0,rows):       # run till the number of arrays
        divide_sum = summation_vertical.item(rows_count,0)      # give the item which divide the element for normailzation
        for i in range(0,columns):                  # run till no of columns in a n-d array
            replace_division = num_arra.item(rows_count,i)/divide_sum  #normalixe the existing value
            num_arra[rows_count,i]  = replace_division                      # replace the new value with exisitng value
    print num_arra    #give cluster array whose sum equal to 1 always
    print num_arra.sum(axis = 1)    
# LDA implimentation 
    model = lda.LDA(n_topics=2, n_iter=10, random_state=2)
    model.fit(x)

    topic_word = model.topic_word_ 
    n_top_words = 11
    
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]    
        fileoutput.write('Topic {}: {}\n'.format(i, ' '.join(topic_words)))
    fileoutput.close()         
term_document_matrix()