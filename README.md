# S3 File Manager 🪣

A Python CLI tool to manage files in AWS S3 — upload, download, delete, list objects, generate presigned URLs, and automatically organize files by type using configurable YAML rules.

---

## Demo

```
$ python3 main.py list --bucket my-bucket

                       S3 Objects Info                        
┏━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Key          ┃ Size     ┃ Last Modified             ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Memoji.jpg   │ 97.53 KB │ 2026-06-16 21:21:03+00:00 │
│ file-pdf.pdf │ 11 KB    │ 2026-06-16 23:35:00+00:00 │
│ file-txt.txt │ 131.0 B  │ 2026-06-16 23:13:00+00:00 │
└──────────────┴──────────┴───────────────────────────┘

$ python3 main.py organize --bucket my-bucket
✓ Files in bucket my-bucket organized successfully based on rules.

$ python3 main.py list --bucket my-bucket

                          S3 Objects Info                          
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Key                  ┃ Size     ┃ Last Modified             ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ docs/file-pdf.pdf    │ 11 KB    │ 2026-06-16 23:35:00+00:00 │
│ docs/file-txt.txt    │ 131.0 B  │ 2026-06-16 23:13:00+00:00 │
│ images/Memoji.jpg    │ 97.53 KB │ 2026-06-16 21:21:03+00:00 │
└──────────────────────┴──────────┴───────────────────────────┘
```

---

## Features

- 📋 List all objects in a bucket with size and last modified date
- ⬆️ Upload local files to S3
- ⬇️ Download objects from S3 to a local destination
- 🗑️ Delete objects from a bucket
- 🔗 Generate temporary presigned URLs for secure file sharing
- 🗂️ Automatically organize files by type using configurable YAML rules
- 📊 Clean terminal output powered by `rich`
- 🔐 Authenticates using a named AWS CLI profile (least privilege IAM user)

---

## Project Structure

```
S3FileManager/
├── manager/
│   ├── __init__.py
│   ├── s3.py            # S3 operations (upload, download, delete, list, presigned URL)
│   ├── organizer.py     # File organization logic with YAML rules
│   └── reporter.py      # Terminal output with rich (tables, messages)
├── config/
│   └── rules.yaml       # Configurable organization rules by file type
├── main.py              # CLI entry point with subcommands
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Technology   | Description                                      |
|--------------|--------------------------------------------------|
| Python 3.10+ | Primary language                                 |
| boto3        | AWS SDK for Python                               |
| rich         | Terminal formatting, tables and styled messages  |
| PyYAML       | YAML configuration file parsing                  |
| pathlib      | Modern file path handling                        |
| argparse     | CLI subcommands and flag handling                |
| AWS S3       | Object storage — all file operations             |

---

## Prerequisites

- Python 3.10+
- AWS CLI v2 installed and configured
- An IAM user with the following permissions:
  - `s3:ListAllMyBuckets`
  - `s3:GetBucketLocation`
  - `s3:ListBucket`
  - `s3:PutObject`
  - `s3:GetObject`
  - `s3:DeleteObject`
  - `s3:CopyObject`

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/jcreyesDev/S3FileManager.git
cd S3FileManager
```

2. Install dependencies:

```bash
pip3 install -r requirements.txt
```

3. Configure your AWS CLI profile:

```bash
aws configure --profile your-profile-name
```

---

## Usage

```bash
# List all objects in a bucket
python3 main.py list --bucket my-bucket

# Upload a file
python3 main.py upload --file ./path/to/file.jpg --bucket my-bucket

# Download a file
python3 main.py download --file photo.jpg --bucket my-bucket --dest ./downloads

# Delete a file
python3 main.py delete --file photo.jpg --bucket my-bucket

# Generate a presigned URL (default expiry: 3600 seconds)
python3 main.py shared-link --file photo.jpg --bucket my-bucket
python3 main.py shared-link --file photo.jpg --bucket my-bucket --expiry 7200

# Organize files by type using rules.yaml
python3 main.py organize --bucket my-bucket

# Show help
python3 main.py --help
```

---

## Configuration — `rules.yaml`

File organization rules are defined in `config/rules.yaml`. Each category specifies a destination prefix and the file extensions that belong to it:

```yaml
rules:
  images:
    prefix: images/
    extensions:
      - .jpg
      - .jpeg
      - .png
      - .gif
      - .webp
  documents:
    prefix: docs/
    extensions:
      - .pdf
      - .docx
      - .txt
      - .xlsx
  videos:
    prefix: videos/
    extensions:
      - .mp4
      - .mov
      - .avi
  others:
    prefix: others/
    extensions: []
```

> Files that don't match any rule are moved to `others/` by default.

---

## IAM Policy

Minimum required permissions for the IAM user running this tool:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets",
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:CopyObject"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## Requirements

- Python 3.10+
- AWS CLI v2
- Active AWS account
- IAM user with minimum required permissions

---

## Author

Developed by [@jcreyesDev](https://github.com/jcreyesDev)