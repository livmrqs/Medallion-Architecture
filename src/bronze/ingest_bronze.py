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

def save_bronze_file(data: bytes) -> None:
    """
    Save the raw JSON file into the Bronze layer locally.
    """

    # Resolve project root dynamically (avoids hardcoded paths)
    base_dir = Path(__file__).resolve().parents[2]

    # Create bronze directory if it does not exist
    bronze_dir = base_dir / "data" / "bronze"
    bronze_dir.mkdir(parents=True, exist_ok=True)

    # Define output file path
    file_path = bronze_dir / "bronze_issues.json"

    # Write raw bytes into file
    with open(file_path, "wb") as file:
        file.write(data)

    print(f"Bronze layer saved successfully at: {file_path}")

def main():
    """
    Main execution flow for Bronze ingestion layer.
    """

    # Step 1: Load configuration
    config = load_environment_variables()

    # Step 2: Create Blob client
    blob_client = get_blob_client(config)

    # Step 3: Download raw data
    raw_data = download_blob(blob_client)

    # Step 4: Persist data locally in Bronze layer
    save_bronze_file(raw_data)


if __name__ == "__main__":
    main()
