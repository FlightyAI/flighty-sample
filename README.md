# Sample repository for flighty

Make sure you have the helm chart installed locally before attempting to run these steps.

## Generate SDK

Create a virtual environment:
```
python3 -m venv env
source env/bin/activate
```

Install swagger code gen:

On Mac:

`brew install swagger-codegen`

Then generate the Python SDK:

```
swagger-codegen generate -i http://localhost/api/v1/openapi.json -l python -o generated-python

# or if running control plane in debugger
swagger-codegen generate -i http://127.0.0.1:8002/openapi.json -l python -o generated-python


```

and install the Python SDK:

```
cd generated-python
python3 setup.py install
cd ..
```

## Run the notebook.

Download the breast cancer dataset:
```
curl https://raw.githubusercontent.com/jbrownlee/Datasets/master/breast-cancer.csv \
     --output breast_cancer.csv           
```

### Testing code locally

First build the image:
```
cd docker_build
docker build . -t gvashishtha/flighty:flighty-demo
cd ..
```

Then actually run it:
```
docker run -p 8001:80 -v /Users/gkv/Startup/flighty-sample/code_sample:/code/customer_code \
-v /Users/gkv/Startup/flighty-sample/model_dir:/code/flighty-files/xgboost/0 \
  gvashishtha/flighty:flighty-demo
```

Then push
`docker push gvashishtha/flighty:flighty-demo`