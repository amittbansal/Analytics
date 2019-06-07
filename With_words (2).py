import Tkinter as tk
import tkFileDialog
import os.path
import shutil
import os             

class Application(tk.Tk):
    def __init__(self, *args, **Kwargs):
        tk.Tk.__init__(self,*args, **Kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frame = {}
        frame=startpage(container,self)
        self.frame[startpage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(startpage)
        
    def show_frame(self,cont):
        frame = self.frame[cont]
        frame.tkraise()

class startpage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller

        f1 = tk.Frame(self)
        f1.pack(fill = "both",side="top",expand = True)
        
        c1 = tk.Canvas(f1,bg="white", height=30, width=40)
        c1.create_line(0,0,4,4)
        c1.pack(anchor="n")
     
        f2 = tk.Frame(f1)
        f2.pack(anchor = "n")
        self.t1 = tk.Text(f2,height=3,width = 50,bd=6,relief = 'raised')
        self.t1.pack(side = "left")
        b1 = tk.Button(f2,text ="Browse File or directory",bd=6,relief = 'raised',command=self.fileinput)
        b1.pack(side = "left")
        
        c2 = tk.Canvas(f1,bg="white", height=30, width=40)
        c2.create_line(0,0,4,4)
        c2.pack(anchor="n")
        
        f3 = tk.Frame(f1)
        f3.pack(anchor = "n")
        self.var = tk.StringVar()
        e2 = tk.Entry(f3,textvariable = self.var,width = 40)
        e2.pack(side = "left")
        b2 = tk.Button(f3, text ="Select output destination",bd=6,relief = 'raised',command=self.fileoutput)
        b2.pack(side = "left")
        
        c1 = tk.Canvas(f1,bg="white", height=30, width=40)
        c1.create_line(0,0,4,4)
        c1.pack(anchor="n")
        
        f4 = tk.Frame(f1)
        f4.pack(anchor = "n")
        l3 = tk.Label(f4, text="Enter the number of Clusters/Topic :",relief = 'raised',bd=6)
        l3.pack(side = "left")
        self.var1 = tk.IntVar()
        e3 = tk.Entry(f4,textvariable = self.var1)
        e3.pack(side = "left")
        
        c1 = tk.Canvas(f1,bg="white", height=30, width=40)
        c1.create_line(0,0,4,4)
        c1.pack(anchor="n")
        
        b4 = tk.Button(f1,text="calculate",bd=6,relief = 'raised',height=3,width = 20,command=self.cal)
        b4.pack(anchor = "n")
        
        c1 = tk.Canvas(f1,bg="black", height=1, width=4000)
        c1.create_line(0,0,4,4)
        c1.pack(anchor="n")
        
        f5 = tk.Frame(f1)
        f5.pack(anchor = "n",fill="both",expand = "yes")
        self.t6 = tk.Text(f5,relief = 'raised',bd=6)
        self.t6.pack(anchor = "n",fill="both",expand = "yes")


    def cal(self):
        self.t6.delete(1.0, 'end')     # clearing the text box fir
        import rpy2.robjects as ro     # connection for R    


        #code to create new file which combine previous selected files at specified location by user
        folder_name = "/123_topic_model_123"
        mypath =self.text + folder_name
        if not os.path.isdir(mypath):
        	os.makedirs(mypath)

        else :
			if os.path.isdir(mypath):
				shutil.rmtree(mypath)
				os.makedirs(mypath)	
        
        save_path=mypath
        self.file1= "Initial.text"
        self.completeName1 = os.path.join(save_path,self.file1)

        # code to merge multiple lines
        list1 = []                     # Empty list     
        text = self.t1.get('1.0', "end-1c").splitlines()
        for line in text:
            list1.append(line)
        with open(self.completeName1, 'w') as outfile:
            for fname in list1:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

        #code to split the files with 5000 documents each                        
        l = 5000
        small = None
        i = 0    
        k = 1       
        with open(self.completeName1) as bi :
            for lineno,line in enumerate(bi):
                if lineno % l == 0 :
                    if small:
                        i = i+1
                        small.close()
                    self.sname = '{}.txt'.format(i)
                    self.completeName2 = os.path.join(save_path,self.sname)
                    small = open(self.completeName2,"w")
                small.write(line)
            if small:
                small.close()

        # r libraries        
        ro.r('library(tm)')
        ro.r('library(svd)')
        ro.r('library(topicmodels)')
        ro.r('library(lsa)')
        ro.r('library(topsis)')
        ro.r('library(fclust)')
        ro.r('library(devtools)')
        ro.r('library(irlba)')
        ro.r('library(skmeans)')
        ro.r('library(data.table)')
        ro.r('library(SnowballC)')
        ro.r('library(wordcloud)')
        ro.r('library(RColorBrewer)')


        ro.r('require(tm)')
        ro.r('require(svd)')
        ro.r('require(topicmodels)')
        ro.r('require(lsa)')
        ro.r('require(topsis)')
        ro.r('require(fclust)')
        ro.r('require(devtools)')
        ro.r('require(irlba)')
        ro.r('require(skmeans)')
        ro.r('require(data.table)')
        ro.r('require(SnowballC)')
        ro.r('require(wordcloud)')
        ro.r('require(RColorBrewer)')


        for x in range(0,i+1): 
            self.oname = '{}.txt'.format(i)
            self.topwordsfile = '{}.txt'.format(i)
            self.completeName3 = os.path.join(save_path,self.oname)          
            with open(self.completeName3,"r") as r:
                noc = self.var1.get()
                ro.r.assign('noc',noc)
                ro.r.assign('self.completeName3',self.completeName3)
                ro.r('mydata <- readLines(self.completeName3)')
                ro.r('corpus <- Corpus(VectorSource(mydata))')
                ro.r('dtm <- DocumentTermMatrix(corpus, control = list(stemming = TRUE, stopwords=TRUE, minWordLength=3,removeNumbers=TRUE, removePunctuation=TRUE))')
                ro.r('matrix0 <- as.matrix(dtm)')
                ro.r('matrix1 <- t(matrix0)')
                ro.r('x <- lw_logtf(matrix1)* gw_idf(matrix1)')
        
                #p(w)       
                ro.r('pword <- 0')
                ro.r('sum_of_rows <- rowSums(x)')
                ro.r('sum_of_matrix <- sum(x)')
                ro.r('for(i in 1:nrow(data.matrix(sum_of_rows))){pword[i]=sum_of_rows[i]/sum_of_matrix}')
        
                #p(d) probability of document
                ro.r('pdoc <- 0')
                ro.r('sum_of_columns <- colSums(x)')
                ro.r('for(i in 1:nrow(data.matrix(sum_of_columns))){pdoc[i]=sum_of_columns[i]/sum_of_matrix}')
        
                #p(w|d)
                ro.r('rows = nrow(x)')
                ro.r('columns = ncol(x)')
                ro.r('pwgd = matrix(rep(0),nrow = rows,ncol = columns)')
                ro.r('for (j in 1:columns){pwgd[i,j]=x[i,j]/sum_of_columns[j]}')

                #deduction technique
                ro.r('dR2 <- irlba(x, 2)')
        
                #clustering p(T|W)
                ro.r('ptgw <- skmeans(dR2$u,k = noc, m = 1.1,control = list(nruns = 5, verbose = TRUE))')  #k in the number of cluster and for accessign the matrix we need $membership
        
                #p(T,W)
                ro.r('A = matrix(rep(0), nrow = nrow(ptgw$membership), ncol = ncol(ptgw$membership))')
                ro.r('for (i in 1:nrow(A)){A[i,] = as.matrix(ptgw$membership[i,]*pword[i])}')
        
                #p(w|t)
                ro.r('B = matrix(rep(0),nrow=nrow(A),ncol = ncol(A))')
                ro.r('Sum_of_columns = colSums(A)')
                ro.r('for (j in 1:ncol(B)){B[,j]=A[,j]/Sum_of_columns[j]}')
        
                #p(t/d)
                ro.r('ptgd = t(ptgw$membership) %*% pwgd')
                ro.r('ptgd = t(ptgd)')

                #writing top 20 words for each topic in file
                self.words = "Newfile.txt"
                self.completeName4 = os.path.join(save_path,self.words)
                ro.r.assign('self.completeName4',self.completeName4)
                ro.r('sink(self.completeName4,append=TRUE)')
                ro.r('for (i in 1:noc){cat("", "",row.names(matrix1)[order(B[,i],decreasing = TRUE)[1:20]],"\n")}')  
                ro.r('sink()')


        ro.r('mydata <- readLines(self.completeName4)')
        ro.r('corpus <- Corpus(VectorSource(mydata))')
        ro.r('dtm <- DocumentTermMatrix(corpus, control = list(stemming = TRUE, stopwords=TRUE, minWordLength=3,removeNumbers=TRUE, removePunctuation=TRUE))')
        ro.r('matrix0 <- as.matrix(dtm)')
        ro.r('matrix1 <- t(matrix0)')
        ro.r('x <- lw_logtf(matrix1)* gw_idf(matrix1)')
        
        #p(w)        
        ro.r('pword <- 0')
        ro.r('sum_of_rows <- rowSums(x)')
        ro.r('sum_of_matrix <- sum(x)')
        ro.r('for(i in 1:nrow(data.matrix(sum_of_rows))){pword[i]=sum_of_rows[i]/sum_of_matrix}')
        
        #p(d) probability of document
        ro.r('pdoc <- 0')
        ro.r('sum_of_columns <- colSums(x)')
        ro.r('for(i in 1:nrow(data.matrix(sum_of_columns))){pdoc[i]=sum_of_columns[i]/sum_of_matrix}')
        
        #p(w|d)
        ro.r('rows = nrow(x)')
        ro.r('columns = ncol(x)')
        ro.r('pwgd = matrix(rep(0),nrow = rows,ncol = columns)')
        ro.r('for (j in 1:columns){pwgd[i,j]=x[i,j]/sum_of_columns[j]}')

        #deduction technique
        ro.r('dR2 <- irlba(x, 2)')
        
        #clustering p(T|W)
        ro.r('ptgw <- skmeans(dR2$u,k = noc, m = 1.1,control = list(nruns = 5, verbose = TRUE))  #k in the number of cluster and for accessign the matrix we need $membership')
        
        #p(T,W)
        ro.r('A = matrix(rep(0), nrow = nrow(ptgw$membership), ncol = ncol(ptgw$membership))')
        ro.r('for (i in 1:nrow(A)){A[i,] = as.matrix(ptgw$membership[i,]*pword[i])}')
        
        #p(w|t)
        ro.r('B = matrix(rep(0),nrow=nrow(A),ncol = ncol(A))')
        ro.r('Sum_of_columns = colSums(A)')
        ro.r('for (j in 1:ncol(B)){B[,j]=A[,j]/Sum_of_columns[j]}')
                
        #p(t/d)
        ro.r('ptgd = t(ptgw$membership) %*% pwgd')
        ro.r('ptgd = t(ptgd)')

        #final top words file
        self.finalwords = "topwords.txt"
        self.completeName5 = os.path.join(save_path,self.finalwords)
        ro.r.assign('self.completeName5',self.completeName5)
        ro.r('sink(self.completeName5,append=TRUE)')
        ro.r('for (i in 1:noc){cat(" ",row.names(matrix1)[order(B[,i],decreasing = TRUE)[1:20]],"\n")}')  
        ro.r('sink()')
    
        # Display the result (top words on the screen)
        top = "topic"
        with open(self.completeName5) as openfile:
            for line in openfile:
                line1 = top + str(" ") + str(k) + str(" ") + line
                self.t6.insert("end",line1)
                k = k + 1
        openfile.close()

        # wordcloud
        ro.r('filePath <- self.completeName5') 
        ro.r('text <- readLines(filePath)')
        ro.r('docs <- Corpus(VectorSource(text))')      #Load the data as a corpus
        ro.r('docs <- tm_map(docs, removeWords, stopwords("english"))') # Remove english common stopwords
        ro.r('docs <- tm_map(docs, stripWhitespace)')  #Eliminate extra white spaces
        ro.r('dtm <- TermDocumentMatrix(docs)') 
        ro.r('m <- as.matrix(dtm)') 
        ro.r('v <- sort(rowSums(m),decreasing=TRUE)') 
        ro.r('d <- data.frame(word = names(v),freq=v)') 
        ro.r('head(d, 10)')
        ro.r('set.seed(1234)')
        ro.r('wordcloud(words = d$word, freq = d$freq, min.freq = 1, max.words=200, random.order=FALSE, rot.per=0.35, colors=brewer.pal(8, "Dark2"))')            

        
    def fileinput(self):
        text = tkFileDialog.askopenfilenames()
        self.li = list(text)
        self.t6.insert("end","Inout Files are :")
        self.t6.insert("end","\n")
        for i in self.li:
            self.t1.insert("end",i)
            self.t1.insert("end","\n")
            self.t6.insert("end",i)
            self.t6.insert("end","\n")
           
    def fileoutput(self):
        self.text = tkFileDialog.askdirectory()
        self.var.set(self.text)
        self.t6.insert("end","\n")
        self.t6.insert("end","Output File location is :")
        self.t6.insert("end","\n")
        self.t6.insert("end",self.text)
        
app = Application()
app.mainloop() 