import argparse
from manager.s3 import list_objects, upload_file, download_file, delete_file, generate_presigned_url
from manager.reporter import print_objects_table, print_success, print_error, print_url
from manager.organizer import organize_bucket

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='S3 File Manager')
    subparsers = parser.add_subparsers(dest='command')
    
    # List
    list_parser = subparsers.add_parser('list', help='List objects in a bucket')
    list_parser.add_argument('--bucket', required=True, help='S3 Bucket name')

    # Upload
    upload_parser = subparsers.add_parser('upload', help='Upload a file to a bucket')
    upload_parser.add_argument('--bucket', required=True, help='S3 Bucket name')
    upload_parser.add_argument('--file', required=True, help='File path to upload')

    # Download
    download_parser = subparsers.add_parser('download', help='Download a file from a bucket')
    download_parser.add_argument('--bucket', required=True, help='S3 Bucket name')
    download_parser.add_argument('--file', required=True, help='File name to download')
    download_parser.add_argument('--dest', required=True, help='Destination path to save the downloaded file')

    # Delete
    delete_parser = subparsers.add_parser('delete', help='Delete a file from a bucket')
    delete_parser.add_argument('--bucket', required=True, help='S3 Bucket name')
    delete_parser.add_argument('--file', required=True, help='File name to delete')

    #Shared link
    shared_parser = subparsers.add_parser('shared-link', help='Generate a presigned URL for a file in a bucket')
    shared_parser.add_argument('--bucket', required=True, help='S3 Bucket name')
    shared_parser.add_argument('--file', required=True, help='File name to generate presigned URL for')
    shared_parser.add_argument('--expiry', type=int, default=3600, help='Expiry time for the presigned URL in seconds')

    #Organize
    organize_parser = subparsers.add_parser('organize', help='Organize files in a bucket based on rules')
    organize_parser.add_argument('--bucket', required=True, help='S3 Bucket name')

    args = parser.parse_args()

    if args.command == 'list':
        objects = list_objects(args.bucket)
        print_objects_table(objects)
    elif args.command == 'upload':
        success = upload_file(args.file, args.bucket)
        if success:
            print_success(f'✓ File {args.file} uploaded successfully to bucket {args.bucket}.')
        else:
            print_error(f'✗ Failed to upload file {args.file} to bucket {args.bucket}.')
    elif args.command == 'download':
        success = download_file(args.file, args.bucket, args.dest)
        if success:
            print_success(f'✓ File {args.file} downloaded successfully from bucket {args.bucket} to {args.dest}.')
        else:
            print_error(f'✗ Failed to download file {args.file} from bucket {args.bucket}.')
    elif args.command == 'delete':
        success = delete_file(args.file, args.bucket)
        if success:
            print_success(f'✓ File {args.file} deleted successfully from bucket {args.bucket}.')
        else:
            print_error(f'✗ Failed to delete file {args.file} from bucket {args.bucket}.')
    elif args.command == 'shared-link':
        url = generate_presigned_url(args.file, args.bucket, args.expiry)
        if url:
            print_url(url)
        else:
            print_error(f'✗ Failed to generate presigned URL for file {args.file} in bucket {args.bucket}.')
    elif args.command == 'organize':
        organize_bucket(args.bucket)
        print_success(f'✓ Files in bucket {args.bucket} organized successfully based on rules.')
    elif args.command is None:
        parser.print_help()