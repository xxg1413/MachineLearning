

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import  KNeighborsClassifier

iris = load_iris()
iris_x = iris.data

#分类 0 1 2 三个类别
iris_y = iris.target
print(iris_y)

```

    [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
     1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2
     2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
     2 2]



```python
x_train, x_test,y_train,y_test = train_test_split(iris_x, iris_y, test_size=0.3) # 7 3分
print(y_train) #打乱的数据

```

    [2 2 0 0 0 1 1 0 1 0 0 1 1 2 0 0 1 2 0 2 2 1 1 2 2 2 1 0 1 1 2 1 2 1 1 1 2
     0 0 0 2 0 2 0 0 2 2 2 1 0 0 2 1 2 2 0 0 2 1 0 2 0 1 1 0 0 0 1 0 2 0 2 0 1
     0 1 1 1 2 1 2 2 0 1 1 0 0 2 1 0 1 2 2 0 2 1 1 1 0 0 2 2 0 2 2]



```python
knn = KNeighborsClassifier()

knn.fit(x_train,y_train)

print(knn.predict(x_test))
print(y_test)

#有一定的误差
```

    [1 2 2 0 2 1 0 0 2 1 1 1 1 0 0 2 2 1 0 1 2 0 2 1 1 1 2 2 0 2 2 1 0 0 0 0 1
     1 1 1 1 2 0 2 2]
    [1 2 2 0 2 1 0 0 2 1 1 1 1 0 0 2 2 1 0 1 2 0 2 1 1 1 2 2 0 2 2 1 0 0 0 0 1
     1 1 1 1 2 0 2 2]

