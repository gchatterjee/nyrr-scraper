import json
import boto3
import logging


logger = logging.getLogger("nyrr-scraper")


S3_CLIENT = boto3.client("s3")
S3_BUCKET = "nyrr-scraper"
S3_FILE = "state.json"


def read_file():
    logger.debug("reading from s3...")
    result = json.loads(
        S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=S3_FILE)["Body"].read()
    )
    logger.debug("read from s3!")
    return result


def write_file(contents):
    logger.debug("writing to s3...")
    result = S3_CLIENT.put_object(Body=contents, Bucket=S3_BUCKET, Key=S3_FILE)
    logger.debug("wrote to s3!")
    return result
