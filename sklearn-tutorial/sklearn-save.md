

```python
from sklearn import  svm
from sklearn import  datasets

```


```python
clf = svm.SVC()
iris = datasets.load_iris()
X,y = iris.data, iris.target
clf.fit(X,y)

```




    SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
      decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
      max_iter=-1, probability=False, random_state=None, shrinking=True,
      tol=0.001, verbose=False)




```python
#导出

import pickle
with open('clf.pickle', 'wb') as f:
    pickle.dump(clf,f)
```


```python
#导入

with open('clf.pickle','rb') as f:
    clf2=pickle.load(f)
    print(clf2.predict(X[0:1]))
    
    
```

    [0]



```python
#sklearn 自带方法
from sklearn.externals import  joblib 

joblib.dump(clf,'clf.pkl')


clf3 = joblib.load('clf.pkl')
print(clf3.predict(X[0:1]))
```

    [0]



```python

```
