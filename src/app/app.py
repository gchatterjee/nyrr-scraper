import json
import logging
from mailer import send_emails
from s3 import write_file
from diff import get_updates
from get_old_states import get_old_states
from get_races import get_races
from get_page_source import get_page_source


def setup_logger():
    logger = logging.getLogger("nyrr-scraper")
    logger.setLevel(logging.DEBUG)


def handler(event, context):
    setup_logger()

    logger = logging.getLogger("nyrr-scraper")

    environment = event["environment"]

    logger.debug("getting page source...")
    page_source = get_page_source()
    logger.debug("got page source!")
    logger.debug("extracting races from page source...")
    new_states = get_races(page_source)
    logger.debug("extracted races from page source!")
    logger.debug("getting old states from s3...")
    old_states = get_old_states(environment)
    logger.debug("got old states from s3!")
    logger.debug("comparing states...")
    updates = get_updates(old_states, new_states)
    logger.debug("compared states!")
    logger.debug("writing new states to s3...")
    state_json = {}
    for key in new_states.keys():
        state_json[key] = json.loads(str(new_states[key]))
    write_file(json.dumps(state_json), environment)
    logger.debug("wrote states to s3!")
    logger.debug("sending messages to subscribers...")
    send_emails(updates, environment)
    logger.debug("sent messages to subscribers!")


if __name__ == "__main__":
    handler(None, None)
