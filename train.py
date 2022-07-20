# binary classification, breast cancer dataset, label and one hot encoded
import joblib
from pandas import read_csv
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.pipeline import make_pipeline


ohe = OneHotEncoder(sparse='false', categories='auto', handle_unknown='ignore')

output_pipeline = LabelEncoder()

# load data
data = read_csv('breast_cancer.csv', header=None)
dataset = data.values

# split data into X and y
X = dataset[:,0:9]
X = X.astype(str)

input_pipeline = make_pipeline(ohe, XGBClassifier())

Y = dataset[:,9]
Y = output_pipeline.fit_transform(Y)

# split data into train and test sets
seed = 7
test_size = 0.33
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

input_pipeline.fit(X_train, y_train)
y_pred = input_pipeline.predict(X_test)
predictions = [round(value) for value in y_pred]

# We should use this at prediction time to construct pydantic types
# print(input_pipeline.get_feature_names_out())
# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
output_pipeline.inverse_transform(y_pred)

joblib.dump(input_pipeline, 'model_dir/input_pipeline.joblib')
joblib.dump(output_pipeline, 'model_dir/output_pipeline.joblib')