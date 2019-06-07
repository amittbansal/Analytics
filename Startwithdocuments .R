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
mydata <- readLines("/Users/Amit/Desktop/small1.txt")

#Document Matrix
corpus <- Corpus(VectorSource(mydata))
dtm <- DocumentTermMatrix(corpus, control = list(stemming = TRUE, stopwords=TRUE, minWordLength=3,removeNumbers=TRUE, removePunctuation=TRUE))
matrix0 <- as.matrix(dtm)
matrix1 <- matrix0

#weightes method
x <- lw_logtf(matrix1)* gw_idf(matrix1)

#p(w probability of word)
pword <- 0
sum_of_columns <- colSums(x)
sum_of_matrix <- sum(x)
for(i in 1:nrow(data.matrix(sum_of_columns)))
{
  pword[i]=sum_of_columns[i]/sum_of_matrix
}

#p(d) probability of document
pdoc <- 0
no_of_documents <- nrow(matrix1)
for(i in 1:no_of_documents)
{
  pdoc[i]=1/no_of_documents
}
#p(w|d)
rows = nrow(x)
columns = ncol(x)
sum_of_rows = rowSums(x)
pwgd = matrix(rep(0),nrow = rows,ncol = columns)
for (i in 1:rows)
  {
    pwgd[i,]=x[i,]/sum_of_rows[i]
  }

#normalization p(w|d)
npwgd = matrix(rep(0),nrow = rows,ncol = columns)
rspwgd = rowSums(pwgd)
for (i in 1:rows)
  {
   npwgd[i,] = pwgd[i,]/rspwgd[i]  
  }

#deduction technique
dR2 <- irlba(x, 2)

#clustering p(T|D)
ptgw <- skmeans(dR2$u,k = 25, m = 1.1,control = list(nruns = 5, verbose = TRUE))  #k in the number of cluster and for accessign the matrix we need $membership

#p(T,D)
A = matrix(rep(0), nrow = nrow(ptgw$membership), ncol = ncol(ptgw$membership))
for (i in 1:nrow(A))
{
  A[i,] = as.matrix(ptgw$membership[i,]*pdoc[i])
}
#p(d|t)
B = matrix(rep(0),nrow=nrow(A),ncol = ncol(A))
Sum_of_columns = colSums(A)
for (j in 1:ncol(B)) 
  {
    B[,j]=A[,j]/Sum_of_columns[j]
  }

#p(w|t)
tpwdt <- t(npwgd)
pwgt <- npwgd %*% B

#top 10 words 

for (i in 1:10)
{
  cat ("topic", i,row.names(matrix1)[order(pwgt[,i],decreasing = TRUE)[1:10]],"\n")
}
