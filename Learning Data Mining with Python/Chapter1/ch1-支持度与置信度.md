

```python
#实现简单的排序规则--支持度和置信度

#在购买记录中寻找顾客同时购买的商品
```


```python
import numpy as np

data_file = "affinity_dataset.txt"

#加载文件
x = np.loadtxt(data_file)
```


```python
#得到特征数量和训练集数量
n_train_test, n_features = x.shape

print(n_train_test, n_features)
```

    100 5



```python
#数据格式  0  1 是否同时购买
print(x[:5])
```

    [[ 0.  0.  1.  1.  1.]
     [ 1.  1.  0.  1.  0.]
     [ 1.  0.  1.  1.  0.]
     [ 0.  0.  1.  1.  1.]
     [ 0.  1.  0.  0.  1.]]



```python
#设置具体features 

features = ['bread','milk','cheese','apples','bananas']

#购买记录为100条

```


```python
#统计多少人买了苹果
num_apples_purchases = 0

for pruchases_recode in x:
    if pruchases_recode[3] == 1:
        num_apples_purchases += 1
    
print("购买苹果的人数为: %d" %(num_apples_purchases))

```

    购买苹果的人数为: 36



```python
#同时购买苹果和香蕉的人数

num_apples_bananas_purchases = 0

for pruchases_recode in x:
    if pruchases_recode[3] == 1  and pruchases_recode[4] == 1:
        num_apples_bananas_purchases += 1
    
print("同时购买苹果和香蕉的人为：%d" % (num_apples_bananas_purchases))

```

    同时购买苹果和香蕉的人为：21



```python
#

confidence = num_apples_bananas_purchases / num_apples_purchases

print("购买苹果的人中，会购买香蕉的人占比: %f" %(100 * confidence))
```

    购买苹果的人中，会购买香蕉的人占比: 58.333333



```python
#应用规则到所有购买产品

from collections import  defaultdict


valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)

n_not_brought=  defaultdict(int)


for pruchases_recode in x:
    for i in range(n_features):
        if pruchases_recode[i] == 0: continue
        n_not_brought[i] += 1
        
        #找到一个购买记录，判断它后面的商品是否购买
        for conclusion in range(n_features):
            if i == conclusion:
                continue
            if pruchases_recode[conclusion] == 1:
                valid_rules[(i, conclusion)] += 1
            else:
                invalid_rules[(i,conclusion)] += 1

#得到支持度
support = valid_rules
confidence = defaultdict(float)

for i, conclusion in valid_rules.keys():
    rule =(i,conclusion)
    #计算置信度
    confidence[rule] = valid_rules[rule] / n_not_brought[i]

    

```


```python
#输出支持度和置信度

for premise, conclusion in confidence:
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    print(" 规则： 如果一个人买了{0}的同时，又买了{1}".format(premise_name, conclusion_name))
    print(" - Confidence: {0:.3f}".format(confidence[(premise, conclusion)]))
    print(" - Support: {0}".format(support[(premise, conclusion)]))
    print("")
```

     规则： 如果一个人买了bread的同时，又买了milk
     - Confidence: 0.519
     - Support: 14
    
     规则： 如果一个人买了milk的同时，又买了cheese
     - Confidence: 0.152
     - Support: 7
    
     规则： 如果一个人买了apples的同时，又买了cheese
     - Confidence: 0.694
     - Support: 25
    
     规则： 如果一个人买了milk的同时，又买了apples
     - Confidence: 0.196
     - Support: 9
    
     规则： 如果一个人买了bread的同时，又买了apples
     - Confidence: 0.185
     - Support: 5
    
     规则： 如果一个人买了apples的同时，又买了bread
     - Confidence: 0.139
     - Support: 5
    
     规则： 如果一个人买了apples的同时，又买了bananas
     - Confidence: 0.583
     - Support: 21
    
     规则： 如果一个人买了apples的同时，又买了milk
     - Confidence: 0.250
     - Support: 9
    
     规则： 如果一个人买了milk的同时，又买了bananas
     - Confidence: 0.413
     - Support: 19
    
     规则： 如果一个人买了cheese的同时，又买了bananas
     - Confidence: 0.659
     - Support: 27
    
     规则： 如果一个人买了cheese的同时，又买了bread
     - Confidence: 0.098
     - Support: 4
    
     规则： 如果一个人买了cheese的同时，又买了apples
     - Confidence: 0.610
     - Support: 25
    
     规则： 如果一个人买了cheese的同时，又买了milk
     - Confidence: 0.171
     - Support: 7
    
     规则： 如果一个人买了bananas的同时，又买了apples
     - Confidence: 0.356
     - Support: 21
    
     规则： 如果一个人买了bread的同时，又买了bananas
     - Confidence: 0.630
     - Support: 17
    
     规则： 如果一个人买了bananas的同时，又买了cheese
     - Confidence: 0.458
     - Support: 27
    
     规则： 如果一个人买了milk的同时，又买了bread
     - Confidence: 0.304
     - Support: 14
    
     规则： 如果一个人买了bananas的同时，又买了milk
     - Confidence: 0.322
     - Support: 19
    
     规则： 如果一个人买了bread的同时，又买了cheese
     - Confidence: 0.148
     - Support: 4
    
     规则： 如果一个人买了bananas的同时，又买了bread
     - Confidence: 0.288
     - Support: 17
    



```python
#分别排序支持度和置信度

# 支持度
from pprint import  pprint
#pprint(list(support.items()))

from operator import  itemgetter
sorted_support = sorted(support.items(), key=itemgetter(1), reverse=True)
pprint(sorted_support)
```

    [((2, 4), 27),
     ((4, 2), 27),
     ((3, 2), 25),
     ((2, 3), 25),
     ((4, 3), 21),
     ((3, 4), 21),
     ((4, 1), 19),
     ((1, 4), 19),
     ((0, 4), 17),
     ((4, 0), 17),
     ((0, 1), 14),
     ((1, 0), 14),
     ((1, 3), 9),
     ((3, 1), 9),
     ((1, 2), 7),
     ((2, 1), 7),
     ((3, 0), 5),
     ((0, 3), 5),
     ((0, 2), 4),
     ((2, 0), 4)]



```python
#置信度
sorted_confience = sorted(confidence.items(), key=itemgetter(1), reverse=True)
pprint(sorted_confience)
                        
```

    [((3, 2), 0.6944444444444444),
     ((2, 4), 0.6585365853658537),
     ((0, 4), 0.6296296296296297),
     ((2, 3), 0.6097560975609756),
     ((3, 4), 0.5833333333333334),
     ((0, 1), 0.5185185185185185),
     ((4, 2), 0.4576271186440678),
     ((1, 4), 0.41304347826086957),
     ((4, 3), 0.3559322033898305),
     ((4, 1), 0.3220338983050847),
     ((1, 0), 0.30434782608695654),
     ((4, 0), 0.288135593220339),
     ((3, 1), 0.25),
     ((1, 3), 0.1956521739130435),
     ((0, 3), 0.18518518518518517),
     ((2, 1), 0.17073170731707318),
     ((1, 2), 0.15217391304347827),
     ((0, 2), 0.14814814814814814),
     ((3, 0), 0.1388888888888889),
     ((2, 0), 0.0975609756097561)]

