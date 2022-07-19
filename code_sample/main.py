from fastapi import File

import flighty
import joblib
import logging
import numpy
import os

from enum import Enum
from pydantic import BaseModel
from xgboost import XGBClassifier

logger = logging.getLogger('customer_main')

class AgeEnum(str, Enum):
    forty249 = '40-49'
    fifty259 = '50-59'
    sixty269 = '60-69'
    seventy279 = '70-79'
    eighty289 = '80-89'
    ninety299 = '90-99'

class MenopauseEnum(str, Enum):
    lessthan40 = 'lt40'
    greaterthan40 = 'ge40'
    premenopause = 'premeno'

class TumorSizeEnum(str, Enum):
    small = '0-4'

class InvolvedNodesEnum(str, Enum):
    small = '0-2'

class NodeCapsEnum(str, Enum):
    yes = 'yes'

class DegMaligEnum(str, Enum):
    ok = '1'
    bad = '2'
    very_bad = '3'

class BreastEnum(str, Enum):
    left = 'left'
    right = 'right'

class BreastQuadEnum(str, Enum):
    leftUp = 'left_up'

class IrradiationEnum(str, Enum):
    yes = 'yes'
    no = 'no'

class Data(BaseModel):
    age: AgeEnum
    meno: MenopauseEnum
    tumor_size: TumorSizeEnum
    inv_nodes: InvolvedNodesEnum
    node_caps: NodeCapsEnum
    deg_malig: DegMaligEnum
    breast: BreastEnum
    breastquad: BreastQuadEnum
    irradiat: IrradiationEnum

model = None
file_path = None

def init():
    '''Sample init method'''
    global model
    global file_path
    logger.info('We just initialized xgboost')
    model = XGBClassifier()
    dir_path = flighty.get_model_path(name='xgboost', version=0)
    logger.info(f"Get model path returns {dir_path}")
    file_path = dir_path
    try:
        logging.info(f"model files are {os.listdir(dir_path)}")
        model.load_model(os.path.join(dir_path, 'xgboost.txt'))
    except FileNotFoundError:
        logging.info(f"artifact directory was not found")


def predict(data : Data):
    '''Sample predict method with pydantic typing'''
    encoded_x = numpy.zeros(shape=43)

    val = [data['age'], data['meno'], data['tumor_size'], data['inv_nodes'], data['node_caps'],
        data['deg_malig'], data['breast'], data['breastquad'], data['irradiat']]
    val = list(map(lambda x: x.value, val))

    encoded_x = numpy.empty(0)
    for i in range(9):
        label_encoder = joblib.load(os.path.join(file_path, f'label-encoder-{i}.joblib'))
        encoder = joblib.load(os.path.join(file_path, f'encoder-{i}.joblib'))
        feature = label_encoder.transform([val[i]])
        feature = feature.reshape(1, 1)
        feature = encoder.transform(feature)
        encoded_x = numpy.append(encoded_x, feature)

    out = model.predict(numpy.expand_dims(encoded_x, axis=0))

    pred_label_encoder = joblib.load(os.path.join(file_path, f'output-label-encoder.joblib'))
    out = pred_label_encoder.inverse_transform(out)
    logger.info('Predict called with data %s, predicted label %s', data, out)
    return (f'Your prediction is {out}')