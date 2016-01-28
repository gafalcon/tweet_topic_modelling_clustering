#https://eight2late.wordpress.com/2015/09/29/a-gentle-introduction-to-topic-modeling-using-r/
#load text mining library
library(tm)
#set working directory
setwd("/mnt/Shared/Gabo/Shared-laptop/Documents/Problemas_Especiales_Computacion/twitter/parsing/csvs");

cluster2 <- read.csv("en_tweets_cluster1.csv", encoding = 'utf-8', stringsAsFactors = FALSE)

#load corpus
#docs <- Corpus(VectorSource(as.character(cluster2$text)));
docs <- Corpus(VectorSource((cluster2$text)));
#inspect a particular document in corpus
writeLines(as.character(docs[[20]]))

#start preprocessing
#Transform to lower case
docs <- tm_map(docs, content_transformer(tolower));

#remove potentially problematic symbols
toSpace <- content_transformer(function(x, pattern) {return (gsub(pattern, " ", x))});
docs <- tm_map(docs, toSpace, "-", lazy = TRUE);
docs <- tm_map(docs, toSpace, "’", lazy = TRUE);
docs <- tm_map(docs, toSpace, "‘", lazy = TRUE);
docs <- tm_map(docs, toSpace, "•", lazy = TRUE);
docs <- tm_map(docs, toSpace, "”", lazy = TRUE);
docs <- tm_map(docs, toSpace, "“", lazy = TRUE);
docs <- tm_map(docs, toSpace, "#", lazy = TRUE);
#remove punctuation
docs <- tm_map(docs, removePunctuation, lazy = TRUE)
#Strip digits
docs <- tm_map(docs, removeNumbers, lazy = TRUE);
#Remove stopwords
docs <- tm_map(docs, removeWords, stopwords("english"), lazy = TRUE);
myStopwords <- c("paris", "isis", "attack", "terrorist");
docs <- tm_map(docs, removeWords, myStopwords, lazy=TRUE);
#Remove whitespace
docs <- tm_map(docs, stripWhitespace, lazy = TRUE);
#Good practice to check every now and then
writeLines(as.character(docs[[20]]))

#Stem document
docs <- tm_map(docs, stemDocument, lazy = TRUE);

writeLines(as.character(docs[[20]]))

#Create document-term matrix
dtm <- DocumentTermMatrix(docs)
# convert rownames to filenames
rownames(dtm) <- cluster2$text;
#collapse matrix by summing over columns
freq <- colSums(as.matrix(dtm));
#length should be total number of terms
length(freq)
#create sord order (descending)
ord <- order(freq, decreasing = TRUE);
#List all terms in decreasing order of freq and write to disk
freq[ord]
write.csv(freq[ord], "word_freq_cluster1.csv")



#load topic models library
library(topicmodels)

# set parameters for Gibbs sampling
burnin <- 4000
iter <- 2000
thin <- 500
seed <- list(2003, 5, 63, 100001, 765)
nstart <- 5
best <- TRUE

#Number of topics
k <- 3

#Run the LDA using Gibbs sampling
ldaOut <- LDA(dtm, k, method="Gibbs", control=list(nstart=nstart, seed=seed, best=best, burnin=burnin, iter=iter, thin=thin))

#write out results
#docs to topics
ldaOut.topics <- as.matrix(topics(ldaOut))

write.csv(ldaOut.topics, file=paste("LDAGibbs", k, "DocsToTopics_cluster1.csv"))

#top 6 terms in each topic
ldaOut.terms <- as.matrix(terms(ldaOut, 6))
write.csv(ldaOut.terms, file=paste("LDAGibbs", k, "TopicsToTerms_cluster1.csv"))

#probabilities associated with each topic assignment
topicProbabilities <- as.data.frame(ldaOut@gamma)
write.csv(topicProbabilities, file=paste("LDAGibbs", k, "TopicProbabilities_cluster1.csv"))

#Find relative importance of top 2 topics
topic1ToTopic2 <- lapply(1:nrow(dtm),function(x)
  sort(topicProbabilities[x,])[k]/sort(topicProbabilities[x,])[k-1])

#Find relative importance of second and third most important topics
topic2ToTopic3 <- lapply(1:nrow(dtm),function(x)
  sort(topicProbabilities[x,])[k-1]/sort(topicProbabilities[x,])[k-2])

#write to file
write.csv(topic1ToTopic2,file=paste("LDAGibbs",k,"Topic1ToTopic2_cluster1.csv"))
write.csv(topic2ToTopic3,file=paste("LDAGibbs",k,"Topic2ToTopic3_cluster1.csv"))
