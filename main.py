
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
    good_evening = get_something_good() and False

    assert good_day == good_night
    assert good_evening != good_day
    logging.info("Now im worried...")
    logger.info("I guess both work HAHHA.")
    logging.info("Wheres good morning???")
