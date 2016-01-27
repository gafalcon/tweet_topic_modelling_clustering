#Db Scan of a single user
library(fossil);
library(dbscan);

latlong <- read.csv("en_tweets.csv"); #Read latlongs of tweets in english

latlong <- latlong[,c(2,1)]; # Reorder columns
    
dist <- earth.dist(latlong[,c(3,4)], dist = T); # calculate distance matrix
kNNdist(dist, k=3, search="kd")
kNNdistplot(dist, k=3)
## the knee is around a distance of .5
    
dens <- dbscan(dist, minPts=3, eps=2); # dbscan to create clusters
print(dens);
latlong$cluster <- dens$cluster; # add column cluster
plot(latlong[,c(3,4)], col=dens$cluster + 1L)
#latlong <- subset(latlong, cluster!=0); # delete rows with cluster == 0
    

#write to csv File
write.csv(latlong, file="en_tweets_clustered.csv")

cluster0 <- subset(latlong, cluster==0); # select rows with cluster == 0
cluster1 <- subset(latlong, cluster==1); # select rows with cluster == 0
cluster2 <- subset(latlong, cluster==2); # select rows with cluster == 0
cluster3 <- subset(latlong, cluster==3); # select rows with cluster == 0

write.csv(latlong, file="en_tweets_cluster0.csv")
write.csv(latlong, file="en_tweets_cluster1.csv")
write.csv(latlong, file="en_tweets_cluster2.csv")
write.csv(latlong, file="en_tweets_cluster3.csv")
