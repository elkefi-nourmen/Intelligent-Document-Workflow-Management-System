import requests
from django.conf import settings

def upload_to_nextcloud(file_path, file_name, username, password, directory):
    """
    Upload a file to Nextcloud using WebDAV.

    Args:
        file_path (str): Local path to the file.
        file_name (str): File name to save on Nextcloud.
        username (str): Nextcloud username or App Password.
        password (str): Nextcloud password.
        directory (str): Directory on Nextcloud to upload to.

    Returns:
        dict: Success status and response.
    """
    base_url = "https://use08.thegood.cloud/remote.php/dav/files/{username}/"
    upload_url = base_url.format(username=username) + directory.strip("/") + "/" + file_name

    try:
        # Open the file and upload using PUT request
        with open(file_path, "rb") as file:
            response = requests.put(upload_url, data=file, auth=(username, password))

        if response.status_code in [200, 201]:
            return {"success": True, "message": "File uploaded successfully.", "url": upload_url}
        else:
            return {"success": False, "message": f"Failed to upload. Status: {response.status_code}", "error": response.text}

    except Exception as e:
        return {"success": False, "message": "An error occurred.", "error": str(e)}