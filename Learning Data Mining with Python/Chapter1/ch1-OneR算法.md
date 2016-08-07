

```python
#OneR算法  其实是OneRule的简写 表示只用许多特征中的一个特征来作为分类依据

#算法思想： 遍历每一个特征的每一个取值，对每一个特征值，统计它在各个类别中出现的次数，找到它出现次数最多的类别
#         并统计它在其他类别中的出现次数

import numpy as np
```


```python
#加载数据

from sklearn.datasets import  load_iris

dataset = load_iris()

#得到数据和输出
X = dataset.data
y = dataset.target

print(dataset.DESCR)
```

    Iris Plants Database
    
    Notes
    -----
    Data Set Characteristics:
        :Number of Instances: 150 (50 in each of three classes)
        :Number of Attributes: 4 numeric, predictive attributes and the class
        :Attribute Information:
            - sepal length in cm
            - sepal width in cm
            - petal length in cm
            - petal width in cm
            - class:
                    - Iris-Setosa
                    - Iris-Versicolour
                    - Iris-Virginica
        :Summary Statistics:
    
        ============== ==== ==== ======= ===== ====================
                        Min  Max   Mean    SD   Class Correlation
        ============== ==== ==== ======= ===== ====================
        sepal length:   4.3  7.9   5.84   0.83    0.7826
        sepal width:    2.0  4.4   3.05   0.43   -0.4194
        petal length:   1.0  6.9   3.76   1.76    0.9490  (high!)
        petal width:    0.1  2.5   1.20  0.76     0.9565  (high!)
        ============== ==== ==== ======= ===== ====================
    
        :Missing Attribute Values: None
        :Class Distribution: 33.3% for each of 3 classes.
        :Creator: R.A. Fisher
        :Donor: Michael Marshall (MARSHALL%PLU@io.arc.nasa.gov)
        :Date: July, 1988
    
    This is a copy of UCI ML iris datasets.
    http://archive.ics.uci.edu/ml/datasets/Iris
    
    The famous Iris database, first used by Sir R.A Fisher
    
    This is perhaps the best known database to be found in the
    pattern recognition literature.  Fisher's paper is a classic in the field and
    is referenced frequently to this day.  (See Duda & Hart, for example.)  The
    data set contains 3 classes of 50 instances each, where each class refers to a
    type of iris plant.  One class is linearly separable from the other 2; the
    latter are NOT linearly separable from each other.
    
    References
    ----------
       - Fisher,R.A. "The use of multiple measurements in taxonomic problems"
         Annual Eugenics, 7, Part II, 179-188 (1936); also in "Contributions to
         Mathematical Statistics" (John Wiley, NY, 1950).
       - Duda,R.O., & Hart,P.E. (1973) Pattern Classification and Scene Analysis.
         (Q327.D83) John Wiley & Sons.  ISBN 0-471-22361-1.  See page 218.
       - Dasarathy, B.V. (1980) "Nosing Around the Neighborhood: A New System
         Structure and Classification Rule for Recognition in Partially Exposed
         Environments".  IEEE Transactions on Pattern Analysis and Machine
         Intelligence, Vol. PAMI-2, No. 1, 67-71.
       - Gates, G.W. (1972) "The Reduced Nearest Neighbor Rule".  IEEE Transactions
         on Information Theory, May 1972, 431-433.
       - See also: 1988 MLC Proceedings, 54-64.  Cheeseman et al"s AUTOCLASS II
         conceptual clustering system finds 3 classes in the data.
       - Many, many more ...
    



```python
#获得记录条数和特征数量

n_samples, n_features = X.shape

print(n_samples, n_features)


```

    150 4



```python
attribute_means = X.mean()
print(attribute_means)

X_d = np.array(X >= attribute_means, dtype='int')
print(X_d.shape)
```

    3.46366666667
    (150, 4)



```python
#分成训练集合和测试集合

from sklearn.cross_validation import  train_test_split 

random_state = 14

X_train,X_test,y_train,y_test = train_test_split(X_d, y, random_state=random_state) #默认25%

print("train:%s\ntest:%s" % (X_train.shape,X_test.shape))
```

    train:(112, 4)
    test:(38, 4)



```python
from collections import  defaultdict
from operator import  itemgetter

def train(X,y_true,feature):
    n_samples, n_features = X.shape
    assert 0 <= feature < n_features
    
    #得到训练集中的不同的值
    values = set(X[:,feature])
    
    predictors = dict()
    errors =[]
        
    
    for current_value in values:
        most_frequent_class,error = train_feauture_value(X,y_true,feature,current_value)
        predictors[current_value] = most_frequent_class
        errors.append(error)
    
    total_error = sum(errors)
    return predictors, total_error


#计算在一个特征值在哪个类别中出现的次数最多
def train_feauture_value(X,y_true, feature, value):
    class_counts = defaultdict(int)
    for sample,y in zip(X,y_true):
        #计算个体在各个类别中的个数
        if sample[feature] == value:
            class_counts[y] += 1
    #排序
    sorted_class_counts = sorted(class_counts.items(), key=itemgetter(1),reverse=True)
    most_frequent_class = sorted_class_counts[0][0]
    
    n_samples = X.shape[1]
    
    #计算在其他类别的次数
    error = sum([ class_counts for class_value,class_counts in class_counts.items() 
                 if class_value != most_frequent_class])
    
    return most_frequent_class, error
    

```


```python
#得到所有的预测值
all_predictors = {variable: train(X_train, y_train, variable) for variable in range(X_train.shape[1])}
errors = {variable: error for variable, (mapping, error) in all_predictors.items()}

#排序所有的测试值
best_variable, best_error = sorted(errors.items(), key=itemgetter(1))[0]
print("The best model is based on variable {0} and has error {1:.2f}".format(best_variable, best_error))

# 选择最好的特征
model = {'variable': best_variable,
         'predictor': all_predictors[best_variable][0]}
print(model)

```

    The best model is based on variable 2 and has error 37.00
    {'predictor': {0: 0, 1: 2}, 'variable': 2}



```python
#使用单一特征预测
def predict(X_test, model):
    variable = model['variable']
    predictor = model['predictor']
    y_predicted = np.array([predictor[int(sample[variable])] for sample in X_test])
    return y_predicted

```


```python
#输出预测值
y_predicted = predict(X_test, model)
print(y_predicted)
```

    [0 0 0 2 2 2 0 2 0 2 2 0 2 2 0 2 0 2 2 2 0 0 0 2 0 2 0 2 2 0 0 0 2 0 2 0 2
     2]



```python
#计算准确度
accuracy = np.mean(y_predicted == y_test) * 100
print("accuracy is %s"  % (accuracy) )
```

    accuracy is 65.7894736842



```python
#输出报告
from sklearn.metrics import  classification_report
print(classification_report(y_test, y_predicted))
```

                 precision    recall  f1-score   support
    
              0       0.94      1.00      0.97        17
              1       0.00      0.00      0.00        13
              2       0.40      1.00      0.57         8
    
    avg / total       0.51      0.66      0.55        38
    


    /Users/xxg/anaconda/lib/python3.5/site-packages/sklearn/metrics/classification.py:1074: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples.
      'precision', 'predicted', average, warn_for)



```python

```
