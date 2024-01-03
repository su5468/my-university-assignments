library('dplyr')
library('ggplot2')


data.cov <- read.csv('covid.csv') %>% filter(Country=='Republic of Korea')
names(data.cov)[1] <- c("Date")
data.cov <- data.cov %>%  mutate(Month = as.integer(substr(Date, 6, 7)), Year = as.factor(substr(Date, 1, 4)), )


bydate <- data.cov %>% group_by(Year, Month) %>% summarize(case=sum(New_cases))
bydate2 <- bydate %>% subset(Year != 2022)


ggplot(data=bydate, aes(x=Month, y=case, color=Year)) + 
  scale_x_continuous(breaks=seq(0, 12, 1)) +
  geom_line() +
  geom_point() +
  facet_wrap(bydate$Year, scales="free_y")+
  theme_test() + 
  labs(title="Fig 1. COVID-19 Cases by Year and Month")+
  theme(plot.title = element_text(hjust=.5, size=20, face="bold"))



ggplot(data=bydate2, aes(x=Month, y=case, color=Year)) + 
  scale_y_continuous(labels=scales::comma, limits=c(0, 200000)) + 
  scale_x_continuous(breaks=seq(0, 12, 1)) +
  geom_line() +
  geom_point() +
  facet_wrap(bydate2$Year, scales="free_y")+
  theme_test() + 
  labs(title="COVID-19 Cases by Year and Month(2020~2021)")+
  theme(plot.title = element_text(hjust=.5, size=20, face="bold"))


ggplot(data=bydate2, aes(x=Month, y=case, color=Year)) + 
  scale_x_continuous(breaks=seq(0, 12, 1)) +
  geom_line() +
  geom_point() +
  facet_wrap(bydate2$Year, scales="free_y")+
  theme_test() + 
  labs(title="Fig 1-1. COVID-19 Cases by Year and Month")+
  theme(plot.title = element_text(hjust=.5, size=20, face="bold"))

