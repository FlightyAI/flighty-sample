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

```

and install the Python SDK:

```
cd generated-python
python3 setup.py install
cd ..
```

Then open a Python REPL and upload an artifact:

```
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(configuration))
file = 'README.md' # str | 
name = 'name_example' # str | 
version = 56 # int | 
type = swagger_client.ArtifactTypeEnum().MODEL

api_instance.create_artifact_artifacts_create_post('README.md', name, version, type)
```