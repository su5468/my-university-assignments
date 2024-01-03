library(readxl)
library(dplyr)
# library(RCurl)
library(httr)
library(stringi)
library(igraph)
library(arules)
library(KoNLP)
library(Sejong)
# Sys.setenv(JAVA_HOME="C:\\Program Files (x86)\\Java\\jre1.8.0_201") # x86
Sys.setenv(JAVA_HOME="C:\\Program Files\\Java\\jre1.8.0_201") # x64
library(rJava)
# library(googleLanguageR)
library(readr)
library(topicmodels)
library(tm)
library(SnowballC)
library(lda)
library(ldatuning)
library(LDAvis)
library(ggplot2)

# ---------------------------------- load data ---------------------------------- #

data.so <- read_excel("사회학전체_t.xls") # read research files
data.so18 <- read_excel("일반2018_t.xls")
data.so19 <- read_excel("일반2019_t.xls")
data.so20 <- read_excel("일반2020_t.xls")
data.so21 <- read_excel("일반2021_t.xls")

data.sono <- rbind(data.so18, data.so19, data.so20, data.so21) # bind files
data.socio <- rbind(data.sono, data.so)
data.socio <- data.socio %>%  mutate(발행년 = as.factor(data.socio$발행년))

data.cov <- read.csv('covid.csv') %>% filter(Country=='Republic of Korea') # read covid file
names(data.cov)[1] <- c("Date") 
data.cov <- data.cov %>%  mutate(Month = as.integer(substr(Date, 6, 7)), Year = as.factor(substr(Date, 1, 4)), )
data.socio <- data.socio[order(data.socio$`발행년`, data.socio$`월`),]
# ---------------------------------- pre-process ---------------------------------- #

trim <-  function (x) gsub("^\\s+|\\s+$", "", x) # function that trim word

for(i in c(1:dim(data.socio)[1])){ 
  word <- data.socio$"키워드(한국어)"[i]
  word <- trim(word) # trim word
  data.socio$"키워드(한국어)"[i] <- gsub("・|․|\n|“|‘|”|’|「|」|『|』|≪|≫|<|>|ㆍ|･|\\.|-|_|ㆍ|#|·|‧|－|‧|《|》", " ",substr(word, 1, nchar(word)-1)) # remove special char(punctuation)
}

str(data.sp)



data.sp %>% group_by(`발행년`, `월`) %>%  summarise(n = n()) %>% ggplot(aes(x=`발행년`, y=`n`, fill=factor(`월`))) +
  geom_col(aes(fill=`발행년`), position='stack') +
  scale_fill_brewer(palette = 'Blues') +
  labs(y='', x='Published Year', title='Published Papers by Year') + 
  theme_classic()+ 
  theme(plot.title=element_text(size=22, hjust=.5, face = 'bold'), legend.position='None')


data.socio <- data.socio %>% filter(nchar(`키워드(한국어)`)>=3)  # remove records without keywords

# ---------------------------------- translation ---------------------------------- #
# 
# translate <- function(api.query, api.lang){ # translation func which uses kakaoapi
#   api.key <- "f5e4f9aa679df383539216a957fd0b74"
#   api.auth <- paste("KakaoAK ", api.key, sep="")
#   api.url <- paste("https://dapi.kakao.com/v2/translation/translate?src_lang=", api.lang, "&target_lang=kr&query=", URLencode(api.query), sep ="")
#   
#   api.res <- httr::GET(api.url,
#                       add_headers("Authorization" = api.auth))
#   return(content(api.res)[[1]][[1]][[1]])
# }
# 
# api.key <- "f5e4f9aa679df383539216a957fd0b74"
# api.auth <- paste("KakaoAK ", api.key, sep="")
# api.url <- paste("https://dapi.kakao.com/v3/translation/language/detect?query=", URLencode(api.query), sep ="")
# 
# 
# for(i in c(1:dim(data.socio)[1])){
#   api.query <- data.socio$"키워드(한국어)"[i]
#   is.eng <- stri_enc_isascii(api.query) # is keywords are eng?
#   if(is.na(is.eng)){
#     print(c(api.query, "is NA")) # if na pass
#   }
#   else if(is.eng){ # if english translate // maybe should translate other langs
#     api.res <- httr::GET(api.url,
#                          add_headers("Authorization" = api.auth))
#     api.lang <- content(api.res)[[1]][[1]]$code
#     # if(content(api.res)[[1]][[1]]$code!="kr"){ 
#     api.lang <- "en"
#     if (is.eng){
#       print(c("original:", api.query))
#       api.tran <- translate(api.query, api.lang)
#       if (!is.na(api.tran) && !is.null(api.tran)){
#         data.socio$"키워드(한국어)"[i] <- api.tran
#       }
#       print(c("translated:", data.socio$"키워드(한국어)"[i]))
#     }
#   }
# }

# ---------------------------------- sec pre-process ---------------------------------- ##

data.sp <- data.socio # kind of backup
data.sp <- data.sp[c(2,12,15,21)] # id, year, keyword, month

for (i in dim(data.sp)[1]){ # removing paren
  data.sp$`키워드(한국어)` <- gsub("\\(.*\\)", "", data.sp$`키워드(한국어)`)
}

# ---------------------------------- split to words ---------------------------------- #

wordbags <- gsub(" ", "", data.sp$`키워드(한국어)`) %>% strsplit(",") # make list of words

# for (i in dim(data.sp)[1]){ # replace comma to whitespace for corpus extraction
#   data.sp$`키워드(한국어)` <- gsub(", ", "  ", data.sp$`키워드(한국어)`)
# }


# quantile(table(unlist(wordbags)), 0.8457) # 15.53% of words are takinng place more than twice

# ---------------------------------- trd pre-process ---------------------------------- #

fc <- function(x) {nchar(x)>=2} # remove 1-length word

filterlen <- function(x){ # filter function
  Filter(fc, x)
}
useNIADic() # using NIA dictionary since it has largest word pool

corpus <- sapply(extractNoun(data.sp$`키워드(한국어)`), filterlen)

# wholebags <- Map(c, corpus, wordbags) 
# wholebags <- Map(unique, wholebags)

# ---------------------------------- conduct a priori algorithm ---------------------------------- #

ul <- unlist(wordbags)[duplicated(unlist(wordbags))]

func <- function(x){
  which(x %in% ul)
}

func2 <- function(x, y){
  x[y]
}

wordbags.ui<-Map(func, wordbags)
wordbags.uu <- Map(func2, wordbags, wordbags.ui)
wordbags.uu <- wordbags.uu[lapply(wordbags.uu, length) > 1]

corpus.ui <- Map(func, corpus)
corpus.uu <- Map(func2, corpus, corpus.ui)
corpus.uu <- corpus.uu[lapply(corpus.uu, length) > 0]

corpus.uu <- unique(corpus.uu)


# for whole data
## non-corpus keywords
wordtran.bags <- as(wordbags.uu, "transactions")
# wordtable.bags <- crossTable(wordtran.bags)
transrules.bags <- apriori(wordtran.bags, parameter = list(support=.0005, conf=.2))
rules.bags <- inspect(transrules.bags)

## corpuses
wordtran.cor <- as(corpus.uu, "transactions")
# wordtable.cor <- crossTable(wordtran.cor)
transrules.cor <- apriori(wordtran.cor, parameter = list(support=.0001, conf=.0001))
rules.cor <- inspect(transrules.cor)
## 1) + 2)?? seems meaningless
# wordtran <- as(wholebags, "transactions")
# # wordtable <- crossTable(wordtran)
# transrules <- apriori(wordtran, parameter = list(support=.0025, conf=.05))
# inspect(transrules)

# divde to pre, post covid
## group covid data by month
data.covid <- data.cov %>% group_by(Year, Month) %>% summarize(
  New_cases=sum(New_cases),
  Cum_cases=max(Cumulative_cases),
  New_deaths=sum(New_deaths),
  Cum_deaths=max(Cumulative_deaths)
)

data.covid <- data.covid[order(data.covid$Year, data.covid$Month),]

data.covid <- data.covid %>% mutate(quarter=ifelse(Month<=3, 1, ifelse(Month<=6, 2, ifelse(Month<=9, 3, 4))))

data.covid.q <- data.covid %>% group_by(Year, quarter) %>% summarize(
  Case = sum(New_cases)
) %>% filter(Year != 2022) %>% mutate(yq=factor(as.numeric(Year)*10 + quarter, levels=c("11","12", "13", "14", "21", "22", "23", "24"), labels = c("20-01", "20-02", "20-03", "20-04", "21-01", "21-02", "21-03", "21-04")))

ggplot(data=data.covid.q, aes(x=yq, y=Case, color=Year)) +
  theme_test()+
  geom_point()+
  geom_line(aes(x=as.numeric(yq),y=Case)) +
  scale_y_continuous(labels=scales::comma) + 
  labs(title = "COVID-19 Cases by Quarter", y='Cases', x='Period') +
  theme(plot.title = element_text(hjust=.5, size=18, face='bold'))

rules.bags <- rules.bags[-2]
interules.bags <- rules.bags %>% filter(lift != 1, lift != '1')
rules.cor <- rules.cor[-2]
interules.cor <- rules.cor %>% filter(lift!=1, lift != '1')

# for pre covid data
# for post covid data



# ----------------------------------  1111  ---------------------------------- #
set.seed(495)

# lexedit <- function(lexicon) {
#   lexicon$vocab<<-gsub("\\(","",lexicon$vocab)
#   lexicon$vocab<<-gsub("c","",lexicon$vocab)
#   lexicon$vocab<<-gsub("\\)","",lexicon$vocab)
#   lexicon$vocab<<-gsub("\"","",lexicon$vocab)
#   lexicon$vocab<<-gsub(",","",lexicon$vocab)
# }

lexicon <- lexicalize(corpus)
lexicon$vocab<-gsub("\\(","",lexicon$vocab)
lexicon$vocab<-gsub("c","",lexicon$vocab)
lexicon$vocab<-gsub("\\)","",lexicon$vocab)
lexicon$vocab<-gsub("\"","",lexicon$vocab)
lexicon$vocab<-gsub(",","",lexicon$vocab)

c(1, 1840, 3650, 5585, 7603)

corpus.prec <- corpus[1:3650]
corpus.postc <- corpus[3651:7603]

lexicon.prec <- lexicalize(corpus.prec)
lexicon.postc <- lexicalize(corpus.postc)

lexicon.prec$vocab<-gsub("\\(","",lexicon.prec$vocab)
lexicon.prec$vocab<-gsub("c","",lexicon.prec$vocab)
lexicon.prec$vocab<-gsub("\\)","",lexicon.prec$vocab)
lexicon.prec$vocab<-gsub("\"","",lexicon.prec$vocab)
lexicon.prec$vocab<-gsub(",","",lexicon.prec$vocab)
lexicon.postc$vocab<-gsub("\\(","",lexicon.postc$vocab)
lexicon.postc$vocab<-gsub("c","",lexicon.postc$vocab)
lexicon.postc$vocab<-gsub("\\)","",lexicon.postc$vocab)
lexicon.postc$vocab<-gsub("\"","",lexicon.postc$vocab)
lexicon.postc$vocab<-gsub(",","",lexicon.postc$vocab)


res.7 <- lda.collapsed.gibbs.sampler(lexicon$documents, 7, lexicon$vocab, 5000, .01, .001,burnin=500, compute.log.likelihood = T)
res.8 <- lda.collapsed.gibbs.sampler(lexicon$documents, 8, lexicon$vocab, 5000, .01, .001,burnin=500, compute.log.likelihood = T)
res.11 <- lda.collapsed.gibbs.sampler(lexicon$documents, 11, lexicon$vocab, 5000, .01, .001, burnin=500, compute.log.likelihood = T)
res.7pre <- lda.collapsed.gibbs.sampler(lexicon.prec$documents, 7, lexicon.prec$vocab, 5000, .01, .001, burnin=500,compute.log.likelihood = T)
res.8pre <- lda.collapsed.gibbs.sampler(lexicon.prec$documents, 8, lexicon.prec$vocab, 5000, .01, .001,burnin=500, compute.log.likelihood = T)
res.13post <- lda.collapsed.gibbs.sampler(lexicon.postc$documents, 13, lexicon.postc$vocab, 5000, .01, .001,burnin=500, compute.log.likelihood = T)
res.7post <- lda.collapsed.gibbs.sampler(lexicon.postc$documents, 7, lexicon.postc$vocab, 5000, .01, .001, burnin=500, compute.log.likelihood = T)

top.topic.words(res.7$topics, 10, by.score = T)
top.topic.words(res.8$topics, 10, by.score = T)
top.topic.words(res.11$topics, 10, by.score = T)
top.topic.words(res.7pre$topics, 10, by.score = T)
top.topic.words(res.8pre$topics, 10, by.score = T)
top.topic.words(res.13post$topics, 10, by.score = T)
top.topic.words(res.7post$topics, 10, by.score = T)

top.topic.words(res.21.12$topics,5, by.score = T)
top.topic.words(res.21.34$topics, 5, by.score = T)

res.7$topic_sums
res.8$topic_sums
res.11$topic_sums
res.7pre$topic_sums
res.8pre$topic_sums
res.13post$topic_sums



# for(i in 2:dim(data.sp)[1]){
#   if(data.sp[i, 2] != data.sp[i-1, 2]){
#     print(c(i, data.sp[i, 2]))
#   }
# }


corpus.19 <- corpus[1840:3649]
corpus.19.12 <-corpus[1840:2699]
corpus.19.34 <-corpus[2700:3649]


corpus.21 <- corpus[5585:7603]
corpus.21.12 <- corpus[5585:6497]
corpus.21.34 <- corpus[6498:7603]

lexicon.19.12 <- lexicalize(corpus.19.12)
lexicon.19.34 <- lexicalize(corpus.19.34)
lexicon.21.12 <- lexicalize(corpus.21.12)
lexicon.21.34 <- lexicalize(corpus.21.34)

lexicon.19.12$vocab<-gsub("\\(","",lexicon.19.12$vocab)
lexicon.19.12$vocab<-gsub("c","",lexicon.19.12$vocab)
lexicon.19.12$vocab<-gsub("\\)","",lexicon.19.12$vocab)
lexicon.19.12$vocab<-gsub("\"","",lexicon.19.12$vocab)
lexicon.19.12$vocab<-gsub(",","",lexicon.19.12$vocab)

lexicon.19.34$vocab<-gsub("\\(","",lexicon.19.34$vocab)
lexicon.19.34$vocab<-gsub("c","",lexicon.19.34$vocab)
lexicon.19.34$vocab<-gsub("\\)","",lexicon.19.34$vocab)
lexicon.19.34$vocab<-gsub("\"","",lexicon.19.34$vocab)
lexicon.19.34$vocab<-gsub(",","",lexicon.19.34$vocab)

lexicon.21.12$vocab<-gsub("\\(","",lexicon.21.12$vocab)
lexicon.21.12$vocab<-gsub("c","",lexicon.21.12$vocab)
lexicon.21.12$vocab<-gsub("\\)","",lexicon.21.12$vocab)
lexicon.21.12$vocab<-gsub("\"","",lexicon.21.12$vocab)
lexicon.21.12$vocab<-gsub(",","",lexicon.21.12$vocab)

lexicon.21.34$vocab<-gsub("\\(","",lexicon.21.34$vocab)
lexicon.21.34$vocab<-gsub("c","",lexicon.21.34$vocab)
lexicon.21.34$vocab<-gsub("\\)","",lexicon.21.34$vocab)
lexicon.21.34$vocab<-gsub("\"","",lexicon.21.34$vocab)
lexicon.21.34$vocab<-gsub(",","",lexicon.21.34$vocab)

res.19.12 <- lda.collapsed.gibbs.sampler(lexicon.19.12$documents, 7, lexicon.19.12$vocab, 5000, .01, .001,burnin=500, compute.log.likelihood = T)
res.19.34 <- lda.collapsed.gibbs.sampler(lexicon.19.34$documents, 7, lexicon.19.34$vocab, 5000, .01, .001,burnin=500, compute.log.likelihood = T)
res.21.12 <- lda.collapsed.gibbs.sampler(lexicon.21.12$documents, 7, lexicon.21.12$vocab, 5000, .01, .001,burnin=500, compute.log.likelihood = T)
res.21.34 <- lda.collapsed.gibbs.sampler(lexicon.21.34$documents, 7, lexicon.21.34$vocab, 5000, .01, .001,burnin=500, compute.log.likelihood = T)

# ----------------------------------  2222  ---------------------------------- #

test <- VCorpus(VectorSource(corpus.21.34))
dtm <- DocumentTermMatrix(test, control=list(
  removePunctuation=TRUE,
  removeNumbers=TRUE, weighting=weightTf))

# t=removeSparseTerms(dtm,0.9999)
t<-dtm
raw.sum=apply(t,1,FUN=sum)
table=t[raw.sum!=0,]

result1 <- FindTopicsNumber(
  table,
  topics = seq(from = 5, to =50, by = 5),
  metrics = c("Griffiths2004", "CaoJuan2009", "Arun2010", "Deveaud2014"),
  method = "Gibbs",
  control = list(seed = 333),
  mc.cores = 8L,
  verbose = TRUE
)
FindTopicsNumber_plot(result1)
result2 <- FindTopicsNumber(               
  table,
  topics = seq(from = 5, to =15, by = 1),
  metrics = c("Griffiths2004", "CaoJuan2009", "Arun2010", "Deveaud2014"),
  method = "Gibbs",
  control = list(seed = 333),
  mc.cores = 8L,
  verbose = TRUE
)
FindTopicsNumber_plot(result2)

lda_data = LDA(table, k=12, method = "Gibbs", control = list(seed=333,burnin=1000,iter=1000,thin=100))

str(lda_data)

# ---------------------------------- plot ---------------------------------- #

visplot <- function(res, lexicon){
  theta <- t(apply(res$document_sums + .01, 2, function(x) x/sum(x)))
  phi <- t(apply(t(res$topics) + .001, 2, function(x) x/sum(x)))
  doc.length <- sapply(lexicon$documents, function(x) sum(x[2, ]))
  
  freq <- c()
  freqtable <- table(lexicon$vocab)
  for(i in 1:length(lexicon$vocab)){
    freq <- append(freq, freqtable[lexicon$vocab[i]])
  }
  
  vis <- list(phi = phi,
              theta = theta,
              doc.length = doc.length,
              vocab = lexicon$vocab,
              term.frequency = freq)
  
  json <- createJSON(phi = vis$phi, 
                     theta = vis$theta, 
                     doc.length = vis$doc.length, 
                     vocab = vis$vocab, 
                     term.frequency = vis$term.frequency)
  
  serVis(json, out.dir = 'vis', open.browser = T)

}

visplot(res.7, lexicon) # 7 or 8
visplot(res.8, lexicon)
visplot(res.11, lexicon)

visplot(res.7pre, lexicon.prec) # 7
visplot(res.8pre, lexicon.prec)

visplot(res.7post, lexicon.postc) # 7
visplot(res.13post, lexicon.postc)

visplot(res.19.12, lexicon.19.12)
visplot(res.19.34, lexicon.19.34)
visplot(res.21.12, lexicon.21.12)
visplot(res.21.34, lexicon.21.34)

# ---------------------------------- use igraph to plot ---------------------------------- #
# size of vertex : freq of word
# distance of vertices : association between words
m = matrix(c(.2,.5,.3, # 순서대로 1, 2, 3번 정점의 x좌표
             .2,.5,.3),        # 순서대로 1, 2, 3번 정점의 y좌표
           nrow=3)       # 정점의 개수 3개
gd=graph(c(1,1,2,2,3,3))  # 자기 자신으로의 루프를 가지고 있는 정점 3개짜리 그래프
plot.igraph(gd, layout=m, add=0) # m의 위치가 적용된 그래프 그리기
