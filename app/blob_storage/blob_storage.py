from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from config import AZURE_CONNECTION_STRING


container_name= 'storagecommoncontainer'
blob_service_client= BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
#container_client= blob_service_client.get_blob_client(container= container_name)