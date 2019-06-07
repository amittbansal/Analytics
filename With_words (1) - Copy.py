import Tkinter as tk
import tkFileDialog
import os.path
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
        self.t6.delete(1.0, 'end')
        import rpy2.robjects as ro
                        
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

        save_path=self.text
        self.file1= "Initial.text"
        self.file2= "wgivent.csv"
        self.file3= "tgivend.csv"
        self.topwords = "topwords.text"

        self.completeName1 = os.path.join(save_path,self.file1)
        self.completeName2 = os.path.join(save_path,self.file2)
        self.completeName3 = os.path.join(save_path,self.file3)
        self.completeName4 = os.path.join(save_path,self.topwords)

        list1 = []
        text = self.t1.get('1.0', "end-1c").splitlines()
        for line in text:
            list1.append(line)
        with open(self.completeName1, 'w') as outfile:
            for fname in list1:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)
        
        self.noc = self.var1.get()
        ro.r.assign('self.noc',self.noc)
        ro.r.assign('self.completeName1',self.completeName1)
        ro.r.assign('self.completeName2',self.completeName2)
        ro.r.assign('self.completeName3',self.completeName3)
        ro.r.assign('self.completeName4',self.completeName4)
                        
        ro.r('mydata <- readLines(self.completeName1)')
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
        ro.r('ptgw <- skmeans(dR2$u,k = self.noc, m = 1.1,control = list(nruns = 5, verbose = TRUE))  #k in the number of cluster and for accessign the matrix we need $membership')
        #p(T,W)
        ro.r('A = matrix(rep(0), nrow = nrow(ptgw$membership), ncol = ncol(ptgw$membership))')
        ro.r('for (i in 1:nrow(A)){A[i,] = as.matrix(ptgw$membership[i,]*pword[i])}')
        #p(w|t)
        ro.r('B = matrix(rep(0),nrow=nrow(A),ncol = ncol(A))')
        ro.r('Sum_of_columns = colSums(A)')
        ro.r('for (j in 1:ncol(B)){B[,j]=A[,j]/Sum_of_columns[j]}')
        ro.r('b<-data.frame(B)')
        ro.r('fwrite(b,self.completeName2)')
        #p(t/d)
        ro.r('ptgd = t(ptgw$membership) %*% pwgd')
        ro.r('ptgd = t(ptgd)')
        ro.r('pd <- data.frame(ptgd)')
        ro.r('fwrite(pd,self.completeName3)')
        #top 10 words 
        ro.r('sink(self.completeName4,append=TRUE)')
        ro.r('write("",self.completeName4, append=FALSE)')
        ro.r('for (i in 1:self.noc){cat("topic", i,row.names(matrix1)[order(B[,i],decreasing = TRUE)[1:self.noc]],"\n")}')
    
        with open(self.completeName4) as openfile:
            for line in openfile:
                self.t6.insert("end",line)
        openfile.close()
        
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