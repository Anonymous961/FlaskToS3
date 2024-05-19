# Upload files to S3 bucket using Flask

Create S3 bucket and set policy for public access. (not necessary but good for you)

- Use IAM for user credentials. Check any YT video ez.

## Install boto3 with pip

```
pip install boto3
```

## Create `.env` file

```py
# in .env file

AWS_BUCKET_NAME=your_bucket_name
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_DOMAIN=http://your_bucket_name.s3.amazonaws.com/
```
