import os
import requests
from urllib.parse import urlparse

def download_files(links, download_folder):
    """
    Downloads files from the given list of links into the specified folder.

    Args:
        links (list): List of file URLs to download.
        download_folder (str): Path to the folder where files will be saved.

    Returns:
        list: List of file paths for the downloaded files.
    """
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    downloaded_files = []
    for link in links:
        try:
            response = requests.get(link, stream=True)
            response.raise_for_status()
            # Extract filename from URL
            parsed_url = urlparse(link)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = "downloaded_file"
            file_path = os.path.join(download_folder, filename)
            # Ensure unique filename
            base, ext = os.path.splitext(file_path)
            counter = 1
            while os.path.exists(file_path):
                file_path = f"{base}_{counter}{ext}"
                counter += 1
            # Write file
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            downloaded_files.append(file_path)
            print(f"Downloaded: {file_path}")
        except Exception as e:
            print(f"Failed to download {link}: {e}")
    return downloaded_files

# Example usage:
if __name__ == "__main__":
    links = [
        "https://example.com/file1.pdf",
        "https://example.com/file2.jpg"
    ]
    download_folder = "downloaded_files"
    download_files(links, download_folder) 