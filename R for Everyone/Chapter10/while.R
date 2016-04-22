use.sumNum <- function(x)
{
  total <- 0
  i <- 0
  
  while (i <= x) {
  
  total <- i + total

  i <- i + 1
}
  
 print(total)
}

use.sumNum(100)
