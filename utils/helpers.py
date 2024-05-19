# in util/helpers.py

import boto3, botocore
import os
from werkzeug.utils import secure_filename


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")


def upload_file_to_s3(file, acl="public-read"):
    filename = secure_filename(file.filename)
    try:
        # Upload the file to S3
        output = s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            filename,
            ExtraArgs={"ContentType": file.content_type},
        )
        print(output)
    except Exception as e:
        # Catch and print any exceptions
        print("Something Happened: ", e)
        return e

    # Return the filename of the uploaded file
    return filename


def download_file_from_s3(filename):
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    download_path = os.path.join("downloads", filename)
    if not os.path.exists("downloads"):
        os.mkdirs("downloads")
    try:
        s3.download_file(bucket_name, filename, download_path)
        return download_path
    except Exception as e:
        print("Something happened: ", e)
        return e


def list_files_in_s3():
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = [content["Key"] for content in response.get("Contents", [])]
        return files
    except Exception as e:
        print("Something happened: ", e)
        return []
