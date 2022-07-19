import swagger_client
from swagger_client.rest import ApiException

import os
import requests
import shutil
import tempfile

from pprint import pprint


DEFAULT_HOSTNAME = "http://127.0.0.1/api/v1"
# create an instance of the API class
api_client = swagger_client.ApiClient()
api_client.configuration.host = DEFAULT_HOSTNAME
api_instance = swagger_client.DefaultApi(api_client)

print(f"""Initializing flighty...
    You are running flighty pointing at the default hostname of {DEFAULT_HOSTNAME}
    To point at your own hostname please run flighty.set_hostname(<your_hostname>)""")

def set_hostname(hostname):
    global api_instance
    api_client.configuration.host = hostname
    api_instance = swagger_client.DefaultApi(api_client)
    print(f"Successfully set hostname to {DEFAULT_HOSTNAME} ")


def create_artifact(path, name, version, type=swagger_client.ArtifactTypeEnum().MODEL):
    raise_if_file(path)
    tmpdir = tempfile.mkdtemp()
    try:
        tmparchive_name = get_tmp_archive(tmpdir, path)
        # Create Artifact
        api_response = api_instance.create_artifact_artifacts_create_post(
            file=tmparchive_name, name=name, version=version, type=type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_artifact_artifacts_create_post: %s\n" % e)
    finally:
        shutil.rmtree(tmpdir)

def list_artifacts():
    try:
        # List Artifacts
        api_response = api_instance.list_artifacts_artifacts_list_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_artifacts_artifacts_list_get: %s\n" % e)

def delete_artifact(name, version):
    body = swagger_client.Artifact(name=name, version=version) # Artifact | 

    try:
        # Delete Artifact
        api_response = api_instance.delete_artifact_artifacts_delete_delete(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_artifact_artifacts_delete_delete: %s\n" % e)


def create_endpoint(name):
    body = swagger_client.EndpointCreate(name=name) # EndpointCreate | 

    try:
        # Create Endpoint
        api_response = api_instance.create_endpoint_endpoints_create_post(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_endpoint_endpoints_create_post: %s\n" % e)

def delete_endpoint(name):
    body = swagger_client.EndpointDelete(name=name) # EndpointDelete | 

    try:
        # Delete Endpoint
        api_response = api_instance.delete_endpoint_endpoints_delete_delete(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_endpoint_endpoints_delete_delete: %s\n" % e)

def list_endpoints():
    try:
        # List Endpoints
        api_response = api_instance.list_endpoints_endpoints_list_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_endpoints_endpoints_list_get: %s\n" % e)

def delete_handler(name, version, endpoint):
    body = swagger_client.HandlerDelete(name=name, version=version, endpoint=endpoint) # HandlerDelete | 

    try:
        # Firsg get name of associated code artifact
        response = get_handler(name=name, endpoint=endpoint, version=version)

        # Delete Handler
        api_response = api_instance.delete_handler_handlers_delete_delete(body)
        pprint(api_response)

        # Then delete artifact
        code_artifact = response.code_artifact
        delete_artifact(name=code_artifact.name, version=code_artifact.version)


    except ApiException as e:
        print("Exception when calling DefaultApi->delete_handler_handlers_delete_delete: %s\n" % e)

def get_handler(name, version, endpoint):
    try:
        # Get Handler
        api_response = api_instance.get_handler_handlers_get_get(name, version, endpoint)
        return api_response
    except ApiException as e:
        print("Exception when calling DefaultApi->get_handler_handlers_get_get: %s\n" % e)

def list_handlers():
    try:
        # List Handlers
        api_response = api_instance.list_handlers_handlers_list_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_handlers_handlers_list_get: %s\n" % e)

def raise_if_file(path):
    '''Raise error if user passes a path to a regular file'''
    if not os.path.isdir(path):
        print("""Path {path} looks like a regular file. 
            Please pass a path to a directory containing your code and try again""")


def get_tmp_archive(tmpdir, path_to_compress):
    tmparchive = os.path.join(tmpdir, 'archive')
    shutil.make_archive(base_name=tmparchive, format='zip', root_dir=path_to_compress)
    return os.path.join(tmpdir, 'archive.zip')

def create_handler(name, endpoint, code_path, version=0, artifacts=[{'name': 'xgboost', 'version': 0}],
    docker_image='docker.io/gvashishtha/flighty:model_server'):
    model_artifact = artifacts[0]['name']
    model_artifact_version = artifacts[0]['version']
    code_artifact = f"{endpoint}-{name}-{version}-code"
    code_artifact_version = 0

    create_artifact(path=code_path, name=code_artifact, version=code_artifact_version, 
        type=swagger_client.ArtifactTypeEnum().CODE)
    body = swagger_client.HandlerCreate(name=name, version=version, endpoint=endpoint,
        model_artifact=model_artifact, model_artifact_version=model_artifact_version,
        docker_image=docker_image, code_artifact=code_artifact, 
        code_artifact_version=code_artifact_version) # HandlerCreate | 

    try:
        # Create Handler
        api_response = api_instance.create_handler_handlers_create_post(body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_handler_handlers_create_post: %s\n" % e)
        

def invoke(endpoint, body):
    return requests.post(f'http://127.0.0.1/{endpoint}/infer', json=body)