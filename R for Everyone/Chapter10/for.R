fruit <- c("apple","banana","pomegranate")

fruitLength <- rep(NA, length(fruit))

print(fruitLength)

names(fruitLength) <- fruit

print(fruitLength)

for (a  in fruit) {
  fruitLength[a] <- nchar(a)
}

print(fruitLength)


