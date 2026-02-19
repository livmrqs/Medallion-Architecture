from pathlib import Path
import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobClient


def load_environment_variables() -> dict:
    """
    Load environment variables from .env file.
    Returns a dictionary with Azure configuration values.
    """
    load_dotenv()

    config = {
        "tenant_id": os.getenv("AZURE_TENANT_ID"),
        "client_id": os.getenv("AZURE_CLIENT_ID"),
        "client_secret": os.getenv("AZURE_CLIENT_SECRET"),
        "account_url": os.getenv("ACCOUNT_URL"),
        "container_name": os.getenv("CONTAINER_NAME"),
        "blob_name": os.getenv("BLOB_NAME"),
    }

    # Validate that all required environment variables are present
    if not all(config.values()):
        raise ValueError("Missing one or more required environment variables.")

    return config
def get_blob_client(config: dict) -> BlobClient:
    """
    Create and return a BlobClient using Service Principal authentication.
    """

    # Create Azure credential using Service Principal
    credential = ClientSecretCredential(
        tenant_id=config["tenant_id"],
        client_id=config["client_id"],
        client_secret=config["client_secret"],
    )

    # Create BlobClient to access the specific blob
    blob_client = BlobClient(
        account_url=config["account_url"],
        container_name=config["container_name"],
        blob_name=config["blob_name"],
        credential=credential,
    )

    return blob_client


def download_blob(blob_client: BlobClient) -> bytes:
    """
    Download the raw file from Azure Blob Storage.
    Returns the file content as bytes.
    """
    return blob_client.download_blob().readall()
