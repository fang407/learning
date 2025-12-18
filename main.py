import os
import time
import json
import logging
logger = logging.getLogger(__name__)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hello! {name}')

def get_something_good():
    print("Get lucky today!")
    logger.warning("Cheeky stuff...")

    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger.warning("Developer debugging...")

    good_day = get_something_good()
    good_night = get_something_good()

    assert good_day == good_night
    print("What happened????")
    logging.info("Now im worried...")
