# -*- coding: utf-8 -*-
"""XGBoost_HeartDisease.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P9RUijfsszy9BrX8FH8VvGtYC0Bosq_v

# XGBOOST: Heart_disease

#Context:

The leading cause of death in the developed world is heart disease. Therefore there needs to be work done to help prevent the risks of of having a heart attack or stroke.

Content: Use this dataset to predict which patients are most likely to suffer from a heart disease in the near future using the features given.

Acknowledgement: This data comes from the University of California Irvine's Machine Learning Repository at https://archive.ics.uci.edu/ml/datasets/Heart+Disease.

source: https://kaggle.com/datasets/rishidamarla/heart-disease-prediction

## O.Importing Libraries
"""

!pip install scikit-optimize

#importing the libraries:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split


import xgboost as xgb
from skopt import BayesSearchCV
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, accuracy_score

"""## 1. Load the dataset:"""

from google.colab import drive
drive.mount('/content/drive')

# Specify the file path
file_path = '/content/drive/Shareddrives/MBD Term2 - Group 6/ML_Group Project/Heart_Disease_Prediction.csv'

# Load the data into a DataFrame
data = pd.read_csv(file_path)

data.head()

data. info()

"""## 2. Visualize data:

### 2.1: Looking into the target variable:
"""

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Countplot to check class balance
sns.countplot(x='Heart Disease', data=data)
plt.show()

HeartDisease_counts = data['Heart Disease'].value_counts()
print(HeartDisease_counts)

"""From this representation we can say that the dataset seems pretty balance, we will keep it as it is for now. However it is important to note that the data set is very small, we will have to take this aspect into consideration while running the model and interpreting the results.

### 2.2: Looking into the other variables:
"""

# Plot 1: Distribution of Age with respect to Heart Disease Presence
plt.figure(figsize=(10,6))
sns.histplot(data=data, x="Age", hue="Heart Disease", element="step", kde=True)
plt.title('Age Distribution by Heart Disease Status')
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()

"""This histogram with a kernel density estimate (KDE) overlay shows the distribution of patients' ages, segmented by the presence or absence of heart disease. The KDE helps to see the probability density of ages. If there is a particular age range with a high density of patients with heart disease compared to those without, as it is the case with teh pick before the 60s, it could suggest that age is a risk factor."""

# Plot 3: Cholesterol Levels by Heart Disease Status
plt.figure(figsize=(10,6))
sns.boxplot(data=data, x="Heart Disease", y="Cholesterol")
plt.title('Cholesterol Levels by Heart Disease Status')
plt.xlabel('Heart Disease')
plt.ylabel('Cholesterol')
plt.show()

"""Suprisinglty this plot shows that cholesterol doesn't seem to be a very important variable, even though we can notice that when there is a heart disease the level of cholesterol is higher."""

# Plot 4: Max Heart Rate by Heart Disease Status
plt.figure(figsize=(10,6))
sns.violinplot(data=data, x="Heart Disease", y="Max HR", split=True)
plt.title('Max Heart Rate by Heart Disease Status')
plt.xlabel('Heart Disease')
plt.ylabel('Max HR')
plt.show()

"""This chart shows the distribution of maximum heart rates for patients with and without heart disease. The thicker sections of the violin plot represent a higher frequency of data points. The group that represents the absence of heart disease has a wider section at higher heart rates and this could indicate that those without heart disease tend to have higher maximum heart rates during exercise. Therefore, this also means that probably the maximum heart rate can be a useful feature in finding out heart disease.

## 3. EDA:

### 3.1: Checking for null values
"""

# Check for missing values
data.isnull().sum()

"""### 3.2: Dealing with categorical variables:"""

data.head()

data.info()

# Encode categorical variables (e.g., one-hot encoding)
data = pd.get_dummies(data, columns=['Chest pain type', 'Heart Disease'], drop_first=True)

#Note that for heart disease: 1=Presence

data.head()

"""3.3 Correlation Matrix:"""

# Let's check the correlation between the variables
# Strong correlation between the mean radius and mean perimeter, mean area and mean primeter
plt.figure(figsize=(20,10))
sns.heatmap(data.corr(), annot=True)

"""From this correlation analysis, we can see that there are not any high correlation in between features. This means there is no need to remove features du to multicolinearity. Let's note high correlation is considered when it is superior to |0.66|.
However the correaltion matrix shows us that one variable is having a very low correlation to our target variable, *FBS over 120* with -0.016 of correlation (fasting blood sugar). However we belive it should be a relevant feature for detecting heart disease. Therefore we decided not to drop it.

## 4. Train/Test Split:
"""

# Split data into features (X) and target (y)
X = data.drop('Heart Disease_Presence', axis=1)
y = data['Heart Disease_Presence']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""Creating an XGBoost Model with Hyperparameter tuning:"""

# Define the XGBoost model
xgb_model = xgb.XGBClassifier()

# Define the hyperparameter search space
param_space = {
    'n_estimators': (10, 1000),  # Number of boosting rounds
    'max_depth': (1, 10),
    'learning_rate': (0.01, 1.0, 'log-uniform'),
    'subsample': (0.5, 1.0, 'uniform'),
    'colsample_bytree': (0.5, 1.0, 'uniform'),
    'gamma': (0, 5, 'uniform'),
    'min_child_weight': (1, 10),
}

# Initialize Bayesian optimization for XGBoost
opt = BayesSearchCV(
    xgb_model,
    param_space,
    n_iter=32,
    cv=5,
    n_jobs=-1)

# Fit the model with Bayesian optimization
opt.fit(X_train, y_train)

# Get the best hyperparameters
best_params = opt.best_params_
best_score = opt.best_score_

print("Best Hyperparameters:", best_params)
print("Best Score (CV Accuracy):", best_score)

# Make 'clf' an instance of the best model.
clf = opt.best_estimator_
clf

# Display the score obtained by the best model.
opt.best_score_

"""## 5. Make Predictions on the test dataset:"""

# Predict the classes of the samples in the test dataset using the best model.
y_test_pred = clf.predict(X_test)
y_test_pred.shape

"""## 6. Construct the confusion matrix and print the classification report:"""

# Removing the seaborn visualization removes the white lines that come with it.
sns.reset_orig()

# Create a confusion matrix
ConfusionMatrixDisplay.from_predictions(
    y_test, y_test_pred,
    labels = clf.classes_,
    cmap = 'magma'
);

"""The confusion matrix provides a summary of the prediction results on a classification problem. The number of correct and incorrect predictions are summarized with count values and broken down by each class. From the above we can say that:
- True Negative (TN): The count of (0,0) = 32 indicates that 32 instances were correctly predicted as no heart disease (Absence).
- False Positive (FP): The count of (0,1) = 1 indicates that 1 instance was incorrectly predicted as having heart disease (Presence) when it actually did not (Absence).
- False Negative (FN): The count of (1,0) = 8 indicates that 8 instances were incorrectly predicted as no heart disease (Absence) when they actually did have it (Presence).
- True Positive (TP): The count of (1,1) = 13 indicates that 13 instances were correctly predicted as having heart disease (Presence).

The confusion matrix is crucial for understanding the model's performance beyond simple accuracy. It shows that the model is relatively conservative, predicting heart disease only when it's quite sure, which is why there are more false negatives (8) than false positives (1).
"""

# Print the classification report with two target names
print(classification_report(y_test, y_test_pred, target_names=['0', '1']))

"""The classification report gives a detailed analysis of the performance of a classification algorithm. From the above we can say that:
- Precision (0): For the 'Absence' of heart disease, the precision is 0.80, meaning that when the model predicts no heart disease, it is correct 80% of the time.
- Recall (0): For the 'Absence' of heart disease, the recall is 0.97, indicating that the model identifies 97% of all actual instances of no heart disease correctly.
- F1-Score (0): The F1-score for 'Absence' is 0.88, which is a weighted average of precision and recall for the 'Absence' class, showing the model's balance between precision and recall for this class.
- Precision (1): For the 'Presence' of heart disease, the precision is 0.93, suggesting that when the model predicts heart disease, it is correct 93% of the time.
- Recall (1): The recall for 'Presence' is 0.62, indicating that the model identifies 62% of all actual instances of heart disease correctly.
- F1-Score (1): The F1-score for 'Presence' is 0.74, showing a balance between precision and recall for the 'Presence' class.
- Accuracy: Overall, the model has an accuracy of 0.83, meaning it correctly predicts the heart disease status 83% of the time across both classes.

**Conclusion:**
The classification report reflects a good model performance, especially considering the precision for predicting the presence of heart disease. However, the model could be improved in terms of recall for the 'Presence' class, as it's missing around 38% of the positive cases. This could be critical in a medical context, where failing to detect heart disease could have serious consequences. However this might also be related to the very small sample we had to train the model. Therefore, in order to improve the model a first step could be to gather more data on the specific topic in order to train the model on a bigger sample.

## 7. Save and export model:
"""

import pickle

filename = 'xgboost_heart_disease_model.sav'
pickle.dump(opt,open(filename,'wb'))