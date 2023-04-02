# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import logging
from typing import List
import boto3
from mailjet_rest import Client
import os
from botocore.exceptions import ClientError
from constants import (
    MAILJET_API_KEY_PUBLIC,
    MAILJET_API_KEY_PRIVATE,
    REGION,
    SENDER,
    SENDER_EMAIL,
    SUBSCRIBER_GROUP_NAME,
)

from update import Update


logger = logging.getLogger("nyrr-scraper")


def check_status(response):
    if not 200 <= response.status_code < 300:
        raise Exception(
            "call to mailerjet API returned {} response".format(response.status_code)
        )


def get_secrets():
    logger.debug("getting secret...")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=REGION)

    try:
        mailjet_public_key = client.get_secret_value(SecretId=MAILJET_API_KEY_PUBLIC)
        mailjet_private_key = client.get_secret_value(SecretId=MAILJET_API_KEY_PRIVATE)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    result = {}
    result["public_key"] = mailjet_public_key["SecretString"]
    result["private_key"] = mailjet_private_key["SecretString"]
    logging.debug("got secret!")
    return result


def get_groups(client):
    response = client.contactslist.get()
    check_status(response)
    result = response.json()["Data"]
    logger.debug("got list of groups!")
    return result


def create_campaign(client, group_id: str, updates: Update):
    logger.debug("creating email campaign...")
    data = {
        "Locale": "en_US",
        "Sender": SENDER,
        "SenderName": SENDER,
        "SenderEmail": SENDER_EMAIL,
        "Subject": "Update to the Race Index",
        "ContactsListID": group_id,
        "Title": "Update to the Race Index",
    }
    response = client.campaigndraft.create(data=data)
    check_status(response)
    campaign_id = response.json()["Data"][0]["ID"]
    logger.debug("created email campaign!")

    logger.debug("writing content to email campaign...")
    html = ["<b>CHANGES TO THE RACE INDEX</b>"]
    for update in updates:
        html.append(str(update))
    html = "<br/><br/>".join(html)
    data = {
        "Headers": "object",
        "Html-part": html,
    }
    response = client.campaigndraft_detailcontent.create(id=campaign_id, data=data)
    check_status(response)
    logger.debug("wrote content to email campaign...")

    logger.debug("launching campaign...")
    response = client.campaigndraft_send.create(id=campaign_id)
    check_status(response)
    logger.debug("launched campaign!")


def send_emails(updates: List[Update], environment: str):
    logger.debug("sending emails...")
    if len(updates) == 0:
        logger.debug("no updates. no emails sent!")
        return
    secrets = get_secrets()
    public_key = secrets["public_key"]
    private_key = secrets["private_key"]
    client = Client(auth=(public_key, private_key))

    groups = get_groups(client)
    subscriber_group = None
    for group in groups:
        if group["Name"] == SUBSCRIBER_GROUP_NAME[environment]:
            subscriber_group = group
    if subscriber_group is None:
        raise Exception(
            "Unable to find group named `{}`".format(SUBSCRIBER_GROUP_NAME[environment])
        )
    create_campaign(client, subscriber_group["ID"], updates)
    logger.debug("emails sent!")
