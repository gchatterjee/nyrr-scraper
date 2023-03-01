# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import logging
import json
from typing import List
import boto3
import requests
from botocore.exceptions import ClientError

from update import Update

SUBSCRIBER_GROUP_NAME = "scraper-subscribers"


logger = logging.getLogger("nyrr-scraper")


def get_secret():
    logger.debug("getting secret...")
    secret_name = "nyrr-scraper/mailerlite-api-token"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    result = get_secret_value_response["SecretString"]
    logging.debug("got secret!")
    return result


def get_groups(token: str):
    logger.debug("getting list of groups...")
    url = "https://connect.mailerlite.com/api/groups"
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.request("GET", url, headers=headers)
    result = response.json()["data"]
    logger.debug("got list of groups!")
    return result


def create_campaign(token: str, group_id: str, updates: Update):
    html = ["<b>CHANGES TO THE RACE INDEX</b>"]
    for update in updates:
        html.append(str(update))
    html = "<br/><br/>".join(html)

    logger.debug("creating email campaign...")
    url = "https://connect.mailerlite.com/api/campaigns"
    payload = json.dumps(
        {
            "name": "Race Updates",
            "type": "regular",
            "emails": [
                {
                    "subject": "Update to the Race Index",
                    "from_name": "Race Updates",
                    "from": "chatterjeegaur@gmail.com",
                    "content": html,
                }
            ],
            "groups": [group_id],
        }
    )
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()["data"]
    logger.debug("created email campaign!")
    return result


def launch_campaign(token: str, campaign_id: str):
    logger.debug("launching campaign...")
    url = "https://connect.mailerlite.com/api/campaigns/{}/schedule".format(campaign_id)
    payload = json.dumps({"delivery": "instant"})
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }
    requests.request("POST", url, headers=headers, data=payload)
    logger.debug("launched campaign!")


def send_emails(updates: List[Update]):
    logger.debug("sending emails...")
    if len(updates) == 0:
        logger.debug("no updates. no emails sent!")
        return
    token = get_secret()
    groups = get_groups(token)
    subscriber_group = None
    for group in groups:
        if group["name"] == SUBSCRIBER_GROUP_NAME:
            subscriber_group = group
    if subscriber_group is None:
        raise Exception("Unable to find group named `{}`".format(SUBSCRIBER_GROUP_NAME))
    campaign = create_campaign(token, subscriber_group["id"], updates)
    launch_campaign(token, campaign["id"])
    logger.debug("emails sent!")
