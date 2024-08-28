
from google.colab import files
uploaded=files.upload()
     


import pandas as pd
data = pd.read_csv('jobss.csv')
print(data.head())
print(data.columns)
     

from sklearn.preprocessing import OneHotEncoder

# Assuming 'df' is your DataFrame and 'column' is the categorical variable column name
encoder = OneHotEncoder()
encoded_data = encoder.fit_transform(data[['Job Title','Job Experience Required','Key Skills','Location','Functional Area','Industry','sal']])

     

from sklearn.preprocessing import OneHotEncoder

# Assuming 'y' is your target variable as a pandas Series
y=data['Role']
encoder = OneHotEncoder(sparse=False)
y_encoded = encoder.fit_transform(y.values.reshape(-1, 1))

     

# Assuming 'encoded_data' is the output of one-hot encoding
df_encoded = pd.concat([data, pd.DataFrame(encoded_data.toarray())], axis=1)

     

from sklearn.preprocessing import OneHotEncoder

# Assuming 'encoder' is your OneHotEncoder object and 'column_names' is the list of original column names
encoded_column_names = encoder.get_feature_names_out()
print(encoded_column_names)

     

# Assuming 'column' is the original categorical column name
df_encoded.drop('Job Title', axis=1, inplace=True)
df_encoded.drop('Job Experience Required', axis=1, inplace=True)
df_encoded.drop('Key Skills', axis=1, inplace=True)
df_encoded.drop('Location', axis=1, inplace=True)
df_encoded.drop('Functional Area', axis=1, inplace=True)
df_encoded.drop('Industry', axis=1, inplace=True)
df_encoded.drop('Role', axis=1, inplace=True)
df_encoded.drop('sal', axis=1, inplace=True)


     

y=y_encoded
x=df_encoded
print(y)
print(x)
     


from sklearn.model_selection import train_test_split
train_X,val_X,train_Y,val_Y=train_test_split(x,y,test_size=0.30,random_state=6)
     

print(train_X.shape)
print(train_Y.shape)
print(val_X.shape)
print(val_Y.shape)
     
(79, 456)
(79, 56)
(34, 456)
(34, 56)

from sklearn.ensemble import RandomForestClassifier
model=RandomForestClassifier(random_state=7,n_estimators=70)
model.fit(train_X,train_Y)
     
RandomForestClassifier(n_estimators=70, random_state=7)

from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(random_state=7)
model.fit(train_X,train_Y)

     
DecisionTreeClassifier(random_state=7)


pred_Y=model.predict(val_X)
import sklearn.metrics as metrics
accuracy=metrics.accuracy_score(val_Y,pred_Y)
print("Accuracy: ",accuracy)
     
Accuracy:  0.5

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

xgb_model = xgb.XGBClassifier()

# Fit the model to the training data
xgb_model.fit(train_X,train_Y)
     


y_pred = xgb_model.predict(val_X)


import sklearn.metrics as metrics
accuracy=metrics.accuracy_score(val_Y,pred_Y)
print("Accuracy: ",accuracy)
     
Accuracy:  0.391304347826087

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=3)

# Train the classifier
knn.fit(train_X,train_Y)
     
KNeighborsClassifier(n_neighbors=3)


from sklearn.metrics import accuracy_score
y_pred = knn.predict(x)

# Calculate the accuracy of the classifier
accuracy = accuracy_score(y, y_pred)
print("Accuracy:", accuracy)
     
Accuracy: 0.336283185840708