

```python
#标准化数据

from sklearn import  preprocessing
import numpy as np

a = np.array([
              [10,2.7, 3.6], 
              [-100,5,-2],
              [120,20,40]
            ], dtype=np.float64)

print(a)
print("标准化数据后：")
print(preprocessing.scale(a))
```

    [[  10.     2.7    3.6]
     [-100.     5.    -2. ]
     [ 120.    20.    40. ]]
    标准化数据后：
    [[ 0.         -0.85170713 -0.55138018]
     [-1.22474487 -0.55187146 -0.852133  ]
     [ 1.22474487  1.40357859  1.40351318]]



```python
from sklearn.cross_validation import  train_test_split
from sklearn.datasets.samples_generator import  make_classification
from sklearn.svm import  SVC
import matplotlib.pyplot as plot

X,y = make_classification(n_samples=300, n_features=2, n_redundant=0, 
                         n_informative=2,random_state=22,n_clusters_per_class=1,scale=100)
```


```python
plot.scatter(X[:,0],X[:,1],c=y)
plot.show()
```


```python
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)
clf = SVC()
clf.fit(X_train,y_train)
print(clf.score(X_test,y_test))
```

    0.444444444444



```python
#压缩范围到-1,1
X = preprocessing.minmax_scale(X,feature_range=(-1,1))
```


```python
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)
clf = SVC()
clf.fit(X_train,y_train)
print(clf.score(X_test,y_test))
```

    0.933333333333



```python
#比较压缩和没压缩数据之后的得分发现压缩之后，得分变高
```
