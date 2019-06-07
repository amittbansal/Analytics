#packages install
library(tm)
library(svd)
library(topicmodels)
library(lsa)
library(topsis)
library(fclust)
library(devtools)
library(irlba)
library(skmeans)
library(data.table)

#getting require modules for library
require(tm)
require(svd)
require(topicmodels)
require(lsa)
require(topsis)
require(fclust)
require(devtools)
require(irlba)
require(skmeans)
require(data.table)

#Reading the file
mydata <- readLines("/Users/Amit/Desktop/a.txt")

#Document Matrix
corpus <- Corpus(VectorSource(mydata))
dtm <- DocumentTermMatrix(corpus, control = list(stemming = TRUE, stopwords=TRUE, minWordLength=3,removeNumbers=TRUE, removePunctuation=TRUE))
matrix0 <- as.matrix(dtm)
matrix1 <- t(matrix0)

#weightes method
x <- lw_logtf(matrix1)* gw_idf(matrix1)

#p(w probability of word)
pword <- 0
sum_of_rows <- rowSums(x)
sum_of_matrix <- sum(x)
for(i in 1:nrow(data.matrix(sum_of_rows)))
{
  pword[i]=sum_of_rows[i]/sum_of_matrix
}

#p(d) probability of document
pdoc <- 0
sum_of_columns <- colSums(x)
for(i in 1:nrow(data.matrix(sum_of_columns)))
{
  pdoc[i]=sum_of_columns[i]/sum_of_matrix
}
#p(w|d)
rows = nrow(x)
columns = ncol(x)
pwgd = matrix(rep(0),nrow = rows,ncol = columns)
for (j in 1:columns)
  {
    pwgd[i,j]=x[i,j]/sum_of_columns[j]
  }

#deduction technique
dR2 <- irlba(x, 2)

#clustering p(T|W)
ptgw <- skmeans(dR2$u,k = 25, m = 1.1,control = list(nruns = 5, verbose = TRUE))  #k in the number of cluster and for accessign the matrix we need $membership

#p(T,W)
A = matrix(rep(0), nrow = nrow(ptgw$membership), ncol = ncol(ptgw$membership))
for (i in 1:nrow(A))
{
  A[i,] = as.matrix(ptgw$membership[i,]*pword[i])
}
#p(w|t)
B = matrix(rep(0),nrow=nrow(A),ncol = ncol(A))
Sum_of_columns = colSums(A)
for (j in 1:ncol(B)) 
      {
        B[,j]=A[,j]/Sum_of_columns[j]
}
b<-data.frame(B)
fwrite(b,"/Users/Amit/Desktop/atest.csv")
#p(t/d)
ptgd = t(ptgw$membership) %*% pwgd
ptgd = t(ptgd)

#top 10 words 
sink("/Users/Amit/Desktop/a.txt",append=TRUE)
for (i in 1:10)
{
  #writeLines(data.frame(cat("topic", i,row.names(matrix1)[order(B[,i],decreasing = TRUE)[1:10]],"\n")),file="/Users/Amit/Desktop/a.txt")
  cat("topic", i,row.names(matrix1)[order(B[,i],decreasing = TRUE)[1:10]],"\n")
}
