#Db Scan of a single user
library(fossil);
library(dbscan);

usr_ids <- list.files(getwd()) #read usrs_ids files
#usr_ids <- read.csv("user_ids", header = FALSE); #Read user ids
#usr_ids <- usr_ids[1][,1]; # transpose column to row
lats <- double(length(usr_ids)); #initialize lats and longs
longs <- double(length(usr_ids));

for (i in 1:length(usr_ids)){
  print(usr_ids[i])
  latlong <- read.csv(as.character(usr_ids[i])); #Read latlongs of user i
  if(length(latlong$lon) > 5){
  latlong <- latlong[,c(2,1)]; # Reorder columns
  
  dist <- earth.dist(latlong, dist = T); # calculate distance matrix
  #kNNdist(dist, k=3, search="kd")
  #kNNdistplot(dist, k=3)
  ## the knee is around a distance of .5
  
  dens <- dbscan(dist, minPts=3, eps=5); # dbscan to create clusters
  print(dens);
  latlong$cluster <- dens$cluster; # add column cluster
  latlong <- subset(latlong, cluster!=0); # delete rows with cluster == 0
  
  # Determine the cluster with most coordinate points
  most_freq <- as.numeric(names(sort(table(latlong$cluster), decreasing = TRUE)[1])); 
  subset(latlong, cluster==most_freq); # Delete rows that are not part of the biggest cluster
  }
  mean_lat <- mean(latlong$lat); # Calculate mean value for lats and longs !!!DANGER!!!
  mean_lon <- mean(latlong$lon);

  lats[i] <- mean_lat; #Add mean values to the arrays
  longs[i] <- mean_lon;
}

# Create a data frame with all user locations
df <- data.frame(usr_ids, lats, longs, stringsAsFactors = FALSE)

#write to csv File
write.csv(df, file="madrid_usrs_locations.csv")
