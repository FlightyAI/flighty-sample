# binary classification, breast cancer dataset, label and one hot encoded
import joblib
import numpy
from pandas import read_csv
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
# load data
data = read_csv('breast_cancer.csv', header=None)
dataset = data.values

# split data into X and y
X = dataset[:,0:9]
X = X.astype(str)
Y = dataset[:,9]

# encode string input values as integers
encoded_x = None
for i in range(0, X.shape[1]):
	label_encoder = LabelEncoder()
	label_encoder.fit(X[:,i])
	joblib.dump(label_encoder, f'model_dir/label-encoder-{i}.joblib')
	feature = label_encoder.transform(X[:,i])
	feature = feature.reshape(X.shape[0], 1)
	onehot_encoder = OneHotEncoder(sparse=False, categories='auto')
	onehot_encoder = onehot_encoder.fit(feature)
	joblib.dump(onehot_encoder, f'model_dir/encoder-{i}.joblib')
	feature = onehot_encoder.transform(feature)
	if encoded_x is None:
		encoded_x = feature
	else:
		encoded_x = numpy.concatenate((encoded_x, feature), axis=1)
print("X shape: : ", encoded_x.shape)

# encode string class values as integers
label_encoder = LabelEncoder()
label_encoder = label_encoder.fit(Y)
joblib.dump(label_encoder, 'model_dir/output-label-encoder.joblib')
label_encoded_y = label_encoder.transform(Y)

# split data into train and test sets
seed = 7
test_size = 0.33
X_train, X_test, y_train, y_test = train_test_split(encoded_x, label_encoded_y, test_size=test_size, random_state=seed)

# fit model no training data
model = XGBClassifier()
model.fit(X_train, y_train)
print(model)

# make predictions for test data
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

model.save_model('model_dir/xgboost.txt')