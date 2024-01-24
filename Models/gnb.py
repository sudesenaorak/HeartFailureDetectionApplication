import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, classification_report, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np
import random

csv_file_path = 'heart.csv'
df = pd.read_csv(csv_file_path)
random.seed(42)
encoder = LabelEncoder()
df['Sex'] = encoder.fit_transform(df['Sex'])
df['ChestPainType'] = encoder.fit_transform(df['ChestPainType'])
df['RestingECG'] = encoder.fit_transform(df['RestingECG'])
df['ExerciseAngina'] = encoder.fit_transform(df['ExerciseAngina'])
df['ST_Slope'] = encoder.fit_transform(df['ST_Slope'])

X = df.drop('HeartDisease', axis=1)
Y = df['HeartDisease']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

nb_classifier = GaussianNB()
nb_classifier.fit(X_train, Y_train)

y_pred = nb_classifier.predict(X_test)

cm = confusion_matrix(Y_test, y_pred)
cm_percent = cm / cm.sum(axis=1)[:, np.newaxis]
cmap = sns.color_palette("Reds", as_cmap=True)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_percent, annot=True, fmt=".2f", cmap=cmap, vmax=1.0, vmin=0.0)
plt.xticks(ticks=[0.5, 1.5], labels=["No Heart Failure", "Heart Failure"])
plt.yticks(ticks=[0.5, 1.5], labels=["No Heart Failure", "Heart Failure"])
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix of Naive Bayes')
plt.show()
print("Confusion Matrix%:\n", cm_percent)

score = accuracy_score(Y_test, y_pred)
f1 = f1_score(Y_test, y_pred)
print("Accuracy:", score)
print("F1-score:", f1)
print(classification_report(Y_test, y_pred))

tn, fp, fn, tp = cm.ravel()
sensitivity = tp / (tp + fn)
print("Sensitivity:", sensitivity)
specificity = tn / (tn + fp)
print("Specificity:", specificity)
precision = tp / (tp + fp)
print("Precision:", precision)
recall = tp / (tp + fn)
print("Recall:", recall)
auc_roc = roc_auc_score(Y_test, y_pred)
print("AUC-ROC:", auc_roc)
train_accuracy = nb_classifier.score(X_train, Y_train)
print("Train Accuracy:", train_accuracy)
cv_scores = cross_val_score(nb_classifier, X_train, Y_train)
print("Mean cross-validation score:", np.mean(cv_scores))
