import collections

import pandas as pd
import pydotplus
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Data collections
# 'segmentId', 'weekday', 'hour', 'isPeakedTime', 'isWeekend', 'congestion'

# importing the dataset

dataset = pd.read_csv('../data/dataset/train_tc_cleaned.csv')


X = dataset.drop('congestion', axis=1)
y = dataset['congestion']

# dataset = pd.read_csv("../data/bill_authentication.csv")
# print(dataset.shape)
# print(dataset.head())

# X = dataset.drop('Class', axis=1)
# y = dataset['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

classifier = tree.DecisionTreeClassifier()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Visualize data
dot_data = tree.export_graphviz(classifier,
                                # feature_names=['Variance','Skewness','Curtosis','Entropy'],
                                feature_names=['segmentId', 'weekday', 'hour', 'isPeakedTime', 'isWeekend'],
                                out_file=None,
                                filled=True,
                                rounded=True)
graph = pydotplus.graph_from_dot_data(dot_data)

colors = ('turquoise', 'orange')
edges = collections.defaultdict(list)

for edge in graph.get_edge_list():
    edges[edge.get_source()].append(int(edge.get_destination()))

for edge in edges:
    edges[edge].sort()
    for i in range(2):
        dest = graph.get_node(str(edges[edge][i]))[0]
        dest.set_fillcolor(colors[i])

graph.write_png('DT.png')

# Prediction
# https://stackabuse.com/decision-trees-in-python-with-scikit-learn/
predict = pd.read_csv("../data/predict/tc_predict.csv")
prediction = classifier.predict(predict)
print(prediction)