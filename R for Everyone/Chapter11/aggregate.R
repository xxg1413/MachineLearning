require(ggplot2)
data("diamonds")
head(diamonds)
aggregate(price ~ cut, diamonds, mean)

aggregate(cbind(price, carat) ~ cut + color, diamonds, mean)
