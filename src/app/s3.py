import json
import boto3
import logging

from constants import S3_FILE, S3_BUCKET


logger = logging.getLogger("nyrr-scraper")


S3_CLIENT = boto3.client("s3")


def read_file(environment: str):
    logger.debug("reading from s3...")
    result = json.loads(
        S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=S3_FILE[environment])["Body"].read()
    )
    logger.debug("read from s3!")
    return result


def write_file(contents, environment: str):
    logger.debug("writing to s3...")
    result = S3_CLIENT.put_object(
        Body=contents, Bucket=S3_BUCKET, Key=S3_FILE[environment]
    )
    logger.debug("wrote to s3!")
    return result
