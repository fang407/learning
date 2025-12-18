# This is a sample Python script.
import time
import os
import json
import logging
logger = logging.getLogger(__name__)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hello! {name}')  # Press ⌘F8 to toggle the breakpoint.

def get_something_good():
    print("Get lucky today!")
    logger.info("Typo happens, but no worries.")

    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("How are you doing??")
    logger.info("Im fine thank you!!! Good practice to print everything out for debug HAHA")
    logger.warning("Warning in your area")
    print("Actually no warning shown in the console, what happened??")
    logger.warning("Developer debugging...")

    good_day = get_something_good()
    good_night = get_something_good()

    assert good_day == good_night
    assert 100 != 101
