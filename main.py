
import logging
logger = logging.getLogger(__name__)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hello! {name}')
    print("Hi John!")

def get_something_good():
    print("Get lucky today!")
    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    good_day = get_something_good()
    good_night = get_something_good()

    assert good_day == good_night
    logger.info("main finished execution.")
