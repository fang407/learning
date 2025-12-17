# This is a sample Python script.

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
    good_day = get_something_good()
    good_evening = get_something_good() or False

    assert good_day == good_evening
