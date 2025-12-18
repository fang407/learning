import os
import logging
logger = logging.getLogger(__name__)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hello! {name}')

def get_something_good():
    print("Get lucky today!")
    logger.warning("Cheeky stuff...")
    logger.info("How to catch AWS timeout in the first place??")

    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger.warning("Developer debugging...")

    good_day = get_something_good()

    assert good_day is True
    assert 23 != 24
    assert 81 != 33

    print("What happened????")
    logging.info("Now im worried...")
    print("Im actually, very very sleepy now. THANK YOU!")
