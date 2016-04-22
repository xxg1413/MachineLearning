use.doubleNum <- function( x ) 
{
   for (i in 1:x) {
     if (i == 1 || i == 2)
     {
       next
     }
     
     if( i == x / 2) {
       break
     }
     
     print(i)
     
   }

}

use.doubleNum(10)