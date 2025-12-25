
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
    logger.warning("Developer debugging...Take naps now!")
    logger.info("Actually, this is to check if we can print log in console.")

    good_day = get_something_good()
    good_night = get_something_good() and False

    assert good_day != good_night
    logging.info("Now im worried...")

