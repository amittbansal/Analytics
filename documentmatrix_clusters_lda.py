import textmining
import numpy as np
import lda
import peach as p
from numpy.random import random
fileinput  = open("test.txt").readlines()
fileoutput = open("output.txt", "wb")

def term_document_matrix():
    num_lines = 0 
    for line in fileinput:
       num_lines = num_lines + 1 
       reading_file_info = [item.rstrip('\n') for item in fileinput]
       tdm = textmining.TermDocumentMatrix()
       for i in range(0,num_lines): 
           tdm.add_doc(reading_file_info[i])
    tdm.write_csv('TermDocumentMatrix.csv',cutoff=1) 
    temp = list(tdm.rows(cutoff=1))
    vocab = tuple(temp[0])
    x=np.array(temp[1:])
    mu = random((num_lines, 3))
    fcm = p.FuzzyCMeans(x, mu, 2)
    print fcm.mu
     
    model = lda.LDA(n_topics=15, n_iter=50, random_state=1)
    model.fit(x)

    topic_word = model.topic_word_ 
    n_top_words = 10
    
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]    
        fileoutput.write('Topic {}: {}\n'.format(i, ' '.join(topic_words)))
    fileoutput.close()          
term_document_matrix()