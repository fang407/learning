# This is a sample Python script.
import logging
logger = logging.getLogger(__name__)
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def get_something_good():
    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("How are you doing??")
    logger.info("Im fine thank you!!! Good practice to print everything out for debug HAHA")
    print("I think we need more retries on model, wdyt?")

    good_day = get_something_good()
    good_night = get_something_good()

    assert good_day == good_night
    assert 2 != 1
    assert good_night is True
