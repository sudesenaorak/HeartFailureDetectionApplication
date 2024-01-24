import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, LeakyReLU
import random

csv_file_path = 'heart.csv'
df = pd.read_csv(csv_file_path)

random.seed(42)
sex = pd.get_dummies(df['Sex'], drop_first = True)
ST_Slope = pd.get_dummies(df['ST_Slope'], drop_first = True)
ExerciseAngina = pd.get_dummies(df['ExerciseAngina'], drop_first = True)
RestingECG = pd.get_dummies(df['RestingECG'], drop_first = True)
ChestPainType = pd.get_dummies(df['ChestPainType'], drop_first = True)

df2 = pd.concat([sex,ST_Slope,ExerciseAngina,RestingECG,ChestPainType],axis = 1)
df = pd.concat([df, df2], axis=1)
df = df.drop(["Sex","ChestPainType","RestingECG","ExerciseAngina","ST_Slope"],axis=1)

X = df.drop('HeartDisease',axis=1)
Y = df['HeartDisease']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

annClassifier = Sequential()
annClassifier.add(Dense(units=3,kernel_initializer='glorot_uniform',activation=LeakyReLU(alpha=0.01),input_dim=X_train.shape[1]))
annClassifier.add(Dense(units=4,kernel_initializer='glorot_uniform',activation=LeakyReLU(alpha=0.01)))
annClassifier.add(Dense(units=1,kernel_initializer='glorot_uniform',activation=LeakyReLU(alpha=0.01)))

annClassifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

model_history = annClassifier.fit(X_train,Y_train,validation_split=0.2,batch_size=10,epochs=80)

print(model_history.history.keys())



plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.legend(['train','test'],loc='lower right')
plt.title('Model Accuracy of ANN')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.show()
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('Model Loss of ANN')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='lower right')
plt.show()

y_pred = annClassifier.predict(X_test)
y_pred = (y_pred > 0.5)

cm = confusion_matrix(Y_test, y_pred)
cm_percent = cm / cm.sum(axis=1)[:, np.newaxis]
cmap = sns.color_palette("Reds", as_cmap=True)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_percent, annot=True, fmt=".2f", cmap=cmap, vmax=1.0, vmin=0.0)
plt.xticks(ticks=[0.5, 1.5], labels=["No Heart Failure", "Heart Failure"])
plt.yticks(ticks=[0.5, 1.5], labels=["No Heart Failure", "Heart Failure"])
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix of ANN')
plt.show()
print("Confusion Matrix%:\n", cm_percent)

score = accuracy_score(y_pred, Y_test)
f1 = f1_score(Y_test, y_pred)
print("Accuracy:", score)
train_accuracy = model_history.history['accuracy']
print("Train Accuracy:", train_accuracy[-1])
print("F1-score:", f1)
print(classification_report(Y_test, y_pred))

annClassifier.save('artificialneural.h5')

tn, fp, fn, tp = cm.ravel()
sensitivity = tp / (tp + fn)
print("Sensitivity:", sensitivity)
specificity = tn / (tn + fp)
print("Specificity:", specificity)
precision = tp / (tp + fp)
print("Precision:", precision)
recall = tp / (tp + fn)
print("Recall:", recall)
roc_auc = roc_auc_score(Y_test, y_pred)
print("ROC-AUC Score:", roc_auc)


val_accuracy = np.mean(model_history.history['val_accuracy'])
print("\n%s: %.2f%%" % ('val_accuracy', val_accuracy*100))

