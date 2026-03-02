import os
import logging
logger = logging.getLogger(__name__)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hello! {name}')

def get_something_good():
    print("Get lucky today! Get test tomorrow!")
    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    good_day = print_hi()
    good_night = get_something_good()

    goodAfternoon = print_hi()

    assert good_day == good_night
    assert True is not False

    logger.error("Script closing, watch out for traffic!")
    print("Script finished execution.")
