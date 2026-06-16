import boto3
import yaml
from manager.s3 import list_objects
from botocore.exceptions import ClientError
from pathlib import Path

def organize_bucket(bucket: str):
    session = boto3.Session(profile_name='jcreyescloud')
    client = session.client('s3')

    with open('config/rules.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    rules = config['rules']
    objects = list_objects(bucket)

    for obj in objects:
        ext = Path(obj['Key']).suffix.lower()

        dest_prefix = 'others/'

        for category, rule in rules.items():
            if ext in rule['extensions']:
                dest_prefix = rule['prefix']
                break
    
        if not obj['Key'].startswith(dest_prefix):
            new_key = dest_prefix + Path(obj['Key']).name

            try:
                client.copy_object(Bucket=bucket, CopySource={'Bucket':bucket, 'Key': obj['Key']}, Key=new_key)
                client.delete_object(Bucket=bucket, Key=obj['Key'])
            except ClientError as e:
                print(e.response['Error']['Message'])