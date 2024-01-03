# okay this sucks... I'll move to rstudio, not cloud
print(a <- 9999) # numeric
print(aa <- 9999L) # integer
print(b <- "helloworld") # string, char
print(T) # bool
# above is atomic vals
# atomic variables are single-element vector

print(c <- c(1,2,3,4,5)) # this is vector
print(m <- matrix(c(1:10), nrow=2)) # this is matrix

# what is markdown?
# markdown is document that has code n description simultaneously

# using other's code (that called package)
# we'll use ggplot2 (for visualization)


head(iris) # this is iris

data <- iris

# i hate rjava***********************
# memorize this**************************
Sys.setenv(JAVA_HOME="C:\\Program Files (x86)\\Java\\jre1.8.0_201")