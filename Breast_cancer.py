"""
# Context:
It is quite common to find ML-based applications embedded with real-time patient data available from different healthcare systems in multiple countries, thereby increasing the efficacy of new treatment options which were unavailable before. This data set is all about predicting whether the cancer cells are benign or malignant.

Content:
Information about attributes:

There are total 10 attributes(int)-
Sample code number: id number
Clump Thickness: 1 - 10, 
Uniformity of Cell Size: 1 - 10, 
Uniformity of Cell Shape: 1 - 10, 
Marginal Adhesion: 1 - 10, 
Single Epithelial Cell Size: 1 - 10, 
Bare Nuclei: 1 - 10, 
Bland Chromatin: 1 - 10, 
Normal Nucleoli: 1 - 10, 
Mitoses: 1 - 10, 
Predicted class:
2 for benign and 4 for malignant

### Importing the libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

"""### Importing the data and preprocessing

The dataset is imported using pandas dataframe, the missing values in this dataset is denoted by '?', Hence, we need to mention what notation is used for the missing values using 'na_value' parameter
"""

dataset = pd.read_csv('breast-cancer-wisconsin.data', na_values='?')
print(dataset.info())

"""This will give us the information about the dataset and the total size of the data. It also shows the non null count by looking at the non null count we can clearly see that the bare nuclei column has missing data.

### Removing the Nan instances

As we observed there are less number of instances which has Nan values, therefore, removing those instances does not impact on the model strength.
"""

null_inds = list(np.where(dataset.isnull())[0])     # Obtained all the Nan indices

dataset = dataset.drop(null_inds)           # removed all Nan indices

print(dataset.info())           # shows no null elements

"""The Outcome in this data is binary but it is represented in 2 and 4 for benign and malignant. We convert that to 0 and 1 to exactly follow binary method."""

outcome = {2: 0, 4: 1}

dataset['class'] = dataset['class'].map(outcome)

"""# Feature to Outcome relationship"""

sns.set(style="ticks", context="talk")
sns.set(font_scale=2)

# All features visualised in for loop

for i in dataset.drop('class', axis=1):
    sns.barplot(y=str(i), x='class', data=dataset)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.show()

"""### Separating the dataset to independent and dependent variables

When separating the data for independent and dependent variables, we need to thoroughly check which column of values is/are not significant for the training and prediction purposes. In the dataset we are considering here the very first column 'code number' which just signifies the patient ID or number which is not helpful for the prediction and is not considered as a feature.

Basically the columns are the attributes or variables, and the rows are the instances
"""

# First let's separate the independent variables from the imported dataset to a variable x
x = dataset.iloc[:, 1:-1].values

# Later the dependent variable is assigned to a variable y
y = dataset.iloc[:, -1].values

# Splitting the data into test and train set

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Feature scaling for the features

# # The main point to consider here is we fit_transform the training set but we only transform the test set,
# # this is to avoid the data leakage to the model from the test set

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

"""# Building the models and Training"""

model_acc = []      # To collect all the model accuracies
model_names = ['Logistic regression', 'KNN', 'kernel SVM',
               'Naive bayes', 'Decision tree', 'Random forest']


def accuracy(predictor):
    # Predicting the test set and making confusion matrix and accuracy score

    from sklearn.metrics import confusion_matrix, accuracy_score

    y_pred = classifier.predict(x_test)
    cm = confusion_matrix(y_pred, y_test)
    # print(cm)
    # print(accuracy_score(y_pred, y_test))

    # Applying K_fold cross validation

    from sklearn.model_selection import cross_val_score

    accuracies = cross_val_score(estimator=predictor, X=x_train, y=y_train, cv=10)

    # print("Accuracy with K-fold: {:.2f} %".format(accuracies.mean() * 100))
    # print("Standard deviation with K-fold: {:.2f} %".format(accuracies.std() * 100))

    model_acc.append(accuracies.mean() * 100)


# Model creation and collecting the accuracies

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


models = [LogisticRegression(), KNeighborsClassifier(n_neighbors=10, metric='minkowski', p=2),
          SVC(kernel='rbf', random_state=0), GaussianNB(), DecisionTreeClassifier(criterion='entropy', random_state=0),
          RandomForestClassifier(n_estimators=1000, min_samples_split=2, min_samples_leaf=4, max_features='auto',
                                 max_depth=None, criterion='entropy', bootstrap=True)]

for i in models:
    classifier = i
    classifier.fit(x_train, y_train)
    accuracy(classifier)

for i in range(len(model_acc)):
    print("model name: {}, accuracy: {:.2f}".format(str(model_names[i]), model_acc[i]))

"""Using model accuracies we can plot a barplot to visualise the accuracies of each model"""

sns.barplot(y=model_names, x=model_acc)
plt.show()

"""As we can see from the barplot all the model accuracies are very close, but the models are capable of reaching upto 97-98% accuracy and here the best accuracy is provided by the KNN model.

The parameters used in the Random forest classification is tuned using Randomised search CV, even though the accuracy is little less than KNN.

As usual we can improve the accuracy by parameter tuning. the next approach will be using an Artificial Neural Network.
"""
