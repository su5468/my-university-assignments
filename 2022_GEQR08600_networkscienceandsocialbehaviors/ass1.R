#install.packages(c("igraph", "poweRlaw", "ggplot2"))

library("igraph")
library("poweRlaw")
library("ggplot2")

# Just loading my data
edge_list <- read.csv("protein.csv", sep="\t", header=0)
G <- graph.data.frame(edge_list)

# List of degrees
G.degrees <- degree(G)

# Let's count the frequencies of each degree
G.degree.histogram <- as.data.frame(table(G.degrees))

# Need to convert the first column to numbers, otherwise
# the log-log thing will not work (that's fair...)
G.degree.histogram[,1] <- as.numeric(G.degree.histogram[,1])

# Now, plot it!

coef(lm(G.degrees~Freq, G.degree.histogram))[2]
co <- coef(lm(log(G.degrees)~log(Freq), G.degree.histogram))[2]


ggplot(G.degree.histogram, aes(x = G.degrees, y = Freq)) +
  geom_point() +
  geom_smooth(method='lm') +
  scale_x_continuous("Degree",
                     breaks = c(1, 10, 100, 1000, 10000),
                     trans = "log10") +
  scale_y_continuous("Frequency",
                     breaks = c(1, 10, 100, 1000, 10000),
                     trans = "log10") +
  ggtitle(paste("Protein Degree Distribution / slope =", -2.2)) +
  theme_bw()
