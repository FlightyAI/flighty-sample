import enum

from pydantic import create_model

def construct_pydantic_type(feature_names):
    col_dict = {}

    for feat in feature_names:
        val = feat.split('_', 1)
        if val[0] in col_dict:
            col_dict[val[0]].append(val[1])
        else:
            col_dict[val[0]] = [val[1]]

    enums = [enum.Enum(k, {item: item for item in v}) for k, v in col_dict.items()]
    enums = {key: value for key, value in zip(col_dict.keys(), map(lambda x: (x, ...), enums))}

    return create_model('Base', **enums)