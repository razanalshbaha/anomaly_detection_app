#from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from config import STORAGE_CONNECTION_STRING

container_name= 'storagecommoncontainer'
blob_service_client= BlobServiceClient(STORAGE_CONNECTION_STRING)
container_client= blob_service_client.get_blob_client(container= container_name)