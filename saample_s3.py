import boto3
from botocore.exceptions import ClientError
import logging
import os
from datetime import datetime

class S3Handler:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name='us-east-1'):
        """
        Initialize S3 client with AWS credentials
        """
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        
    def create_folder(self, bucket_name, folder_name):
        """
        Create a folder in S3 bucket (S3 doesn't have real folders, so we create an empty object)
        
        Parameters:
        - bucket_name: Name of the S3 bucket
        - folder_name: Name of the folder to create
        
        Returns:
        - bool: True if folder was created, else False
        """
        try:
            # Ensure folder name ends with '/'
            if not folder_name.endswith('/'):
                folder_name += '/'
            
            # Create an empty object with the folder name (this creates the "folder")
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=folder_name
            )
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def upload_file_to_folder(self, file_path, bucket_name, folder_name, s3_file_name=None):
        """
        Upload a file to a specific folder in S3 bucket
        
        Parameters:
        - file_path: Local path of the file to upload
        - bucket_name: Name of the S3 bucket
        - folder_name: Name of the folder to upload to
        - s3_file_name: Name to give the file in S3 (if None, uses original filename)
        
        Returns:
        - bool: True if file was uploaded, else False
        - str: Public URL of the file if upload successful, else error message
        """
        try:
            # Ensure folder name ends with '/'
            if not folder_name.endswith('/'):
                folder_name += '/'
            
            # If s3_file_name is not provided, use the original file name
            if s3_file_name is None:
                s3_file_name = os.path.basename(file_path)
            
            # Create the full S3 key (path) for the file
            s3_key = folder_name + s3_file_name
            
            # Upload the file
            self.s3_client.upload_file(
                file_path,
                bucket_name,
                s3_key,
                ExtraArgs={'ACL': 'public-read'}
            )
            
            # Generate the URL for the uploaded file
            url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
            return True, url
            
        except ClientError as e:
            logging.error(e)
            return False, str(e)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return False, str(e)

    def upload_fileobj_to_folder(self, file_obj, bucket_name, folder_name, s3_file_name):
        """
        Upload a file-like object to a specific folder in S3 bucket
        
        Parameters:
        - file_obj: File-like object to upload
        - bucket_name: Name of the S3 bucket
        - folder_name: Name of the folder to upload to
        - s3_file_name: Name to give the file in S3
        
        Returns:
        - bool: True if file was uploaded, else False
        - str: Public URL of the file if upload successful, else error message
        """
        try:
            # Ensure folder name ends with '/'
            if not folder_name.endswith('/'):
                folder_name += '/'
            
            # Create the full S3 key (path) for the file
            s3_key = folder_name + s3_file_name
            
            self.s3_client.upload_fileobj(
                file_obj,
                bucket_name,
                s3_key,
                ExtraArgs={'ACL': 'public-read'}
            )
            
            url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
            return True, url
            
        except ClientError as e:
            logging.error(e)
            return False, str(e)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return False, str(e)

    def list_files_in_folder(self, bucket_name, folder_name):
        """
        List all files in a specific folder
        
        Parameters:
        - bucket_name: Name of the S3 bucket
        - folder_name: Name of the folder to list files from
        
        Returns:
        - list: List of file names in the folder
        """
        try:
            # Ensure folder name ends with '/'
            if not folder_name.endswith('/'):
                folder_name += '/'
            
            response = self.s3_client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=folder_name
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    # Remove the folder prefix from the file name
                    file_name = obj['Key'].replace(folder_name, '')
                    if file_name:  # Don't include the folder itself
                        files.append(file_name)
            
            return files
        except ClientError as e:
            logging.error(e)
            return []

# Example usage:
if __name__ == "__main__":
    import os
    # Replace these with your actual AWS credentials
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')      
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    
    # Initialize S3 handler
    s3_handler = S3Handler(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    
    # Example: Create a folder with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    folder_name = f"uploads/{current_date}"
    
    # Create the folder
    if s3_handler.create_folder(BUCKET_NAME, folder_name):
        print(f"Folder '{folder_name}' created successfully")
    else:
        print(f"Failed to create folder '{folder_name}'")
    
    # Example: Upload a file to the created folder
    success, result = s3_handler.upload_file_to_folder(
        file_path=r"C:\Users\Admin\Downloads\Doraemon.txt",
        bucket_name=BUCKET_NAME,
        folder_name=folder_name
    )
    
    if success:
        print(f"File uploaded successfully to folder. URL: {result}")
    else:
        print(f"Upload failed: {result}")
    
    # Example: List files in the folder
    files = s3_handler.list_files_in_folder(BUCKET_NAME, folder_name)
    print(f"Files in folder '{folder_name}': {files}") 