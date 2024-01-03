library('dplyr')
library('ggplot2')
library('readxl')
library('wordcloud2')
library('stringr')
library("splitstackshape")
library("tidyverse")

data.so <- read_excel("사회학전체.xls")
data.so18 <- read_excel("일반2018.xls")
data.so19 <- read_excel("일반2019.xls")
data.so20 <- read_excel("일반2020.xls")
data.so21 <- read_excel("일반2021.xls")

data.sono <- rbind(data.so18, data.so19, data.so20, data.so21)
data.socio <- rbind(data.sono, data.so)

data.socio <- data.socio %>%  mutate(발행년 = as.factor(data.socio$발행년))

sociodate <- data.socio %>% group_by(발행년, 월) %>% summarize(n = n())


### fig2
ggplot(data=sociodate, aes(x=월, y=n, group=발행년)) +
  scale_x_continuous(breaks=seq(0, 12, 1)) +
  geom_line(aes(color=발행년, shape=발행년))+
  geom_point(size=3, aes(color=발행년, shape=발행년))+
  theme_test() + 
  labs(title="Fig 2. Change in The Number of Sociology Academic Papers", x= "Month", y="Published Papers", color="Year", shape="Year")+
  theme(plot.title = element_text(hjust=.5, size=20, face="bold"))


help(geom_bar)

data.subject <- data.socio[,17]
data.subject %>% group_by(주제분야) %>% summarize(n=n())

data.words <- data.socio[,16] %>% mutate(word = "")
names(data.words)[1] <- c("words")
data.words <- data.words %>% mutate(words = ifelse(data.words$words==",,", "", data.words$words))
data.words <- data.words %>% filter(words != "", words != " ", words != ", ,", words != ",.,")
data.split <- str_split(data.words[,1], pattern=',')
cSplit(indt=data.words, splitCols = "word", sep= ",")

data.freq <- data.frame(matrix(unlist(data.split)), nrow=length(data.split))
data.freq <- data.freq[-1,]
names(data.freq) <- c("word", "nrow")
data.freq <- data.freq %>% filter(length(word) > 3, word !=  " \n\"")
data.freq <- data.freq %>% filter(word != " \"", word != "\"")

data.freq <- data.freq %>% mutate(word = tolower(word))

byfreq <- data.freq %>% group_by(word) %>% summarize(n=n())

byfreq <- byfreq %>% filter(!str_detect(word, "<u+"))

str(byfreq[order(-byfreq$n), ])

freqlarge <- byfreq %>% filter(n > 1)
freqtwo <- freqlarge %>% filter(n>2)

freqtwo <- freqtwo[order(-freqtwo$n),]
### fig3
wordcloud2(byfreq, size=2)
wordcloud2(freqlarge, size=0.3)
wordcloud2(freqtwo, size=0.5, shape="cardiod", color = "random-light", backgroundColor = "black")
