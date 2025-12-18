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
    print_hi('Layer is indeed not to mess around with.')
    print("How are you doing!")
    logger.info("Im fine thank you!!!")

    good_day = get_something_good()
    good_night = get_something_good()

    assert good_day == good_night
    assert 2 != 1
    assert 3 == 3
