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