import boto3
from botocore.exceptions import ClientError
from pathlib import Path

def list_objects(bucket: str):
    session = boto3.Session(profile_name='jcreyescloud')
    client = session.client('s3')

    try:
        paginator = client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket)
        objects = []

        for page in pages:
            for obj in page.get('Contents', []):
                objects.append(obj)

        return objects
    except ClientError as e:
        print(e.response['Error']['Message'])
        
        return []
    
def upload_file(file_path: str, bucket: str) -> bool:
    session = boto3.Session(profile_name='jcreyescloud')
    client = session.client('s3')

    try:
        path = Path(file_path)
        client.upload_file(file_path, bucket, path.name)
        
        return True
    except ClientError as e:
        print(e.response['Error']['Message'])
        
        return False

def download_file(file_name: str, bucket: str, dest: str) -> bool:
    session = boto3.Session(profile_name='jcreyescloud')
    client = session.client('s3')

    try:
        dest_path = Path(dest) / file_name
        client.download_file(bucket, file_name, str(dest_path))
        
        return True
    except ClientError as e:
        print(e.response['Error']['Message'])
        
        return False
    
def delete_file(file_name: str, bucket: str) -> bool:
    session = boto3.Session(profile_name='jcreyescloud')
    client = session.client('s3')

    try:
        client.delete_object(Bucket=bucket, Key=file_name)
        
        return True
    except ClientError as e:
        print(e.response['Error']['Message'])

        return False

def generate_presigned_url(file_name: str, bucket: str, expires: int = 3600) -> str | None:
    session = boto3.Session(profile_name='jcreyescloud')
    client = session.client('s3')
    
    try:
        url = client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': file_name}, ExpiresIn=expires)

        return url
    except ClientError as e:
        print(e.response['Error']['Message'])

        return None

