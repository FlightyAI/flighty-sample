from .helper import construct_pydantic_type
import flighty
import joblib
import os

dir_path = flighty.get_model_path(name='xgboost', version=0)
input_pipeline = joblib.load(os.path.join(dir_path, 'input_pipeline.joblib'))

feature_names = input_pipeline[0].get_feature_names_out()
Data = construct_pydantic_type(feature_names)
output_pipeline = None

def init():
    '''Sample init method'''
    global output_pipeline
    output_pipeline = joblib.load(os.path.join(dir_path, 'output_pipeline.joblib'))


def predict(data : Data):
    '''Sample predict method with pydantic typing'''
    out = input_pipeline.predict([list(data.values())])
    out = output_pipeline.inverse_transform(out)
    return (f'Your prediction is {out}')