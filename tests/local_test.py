from datetime import datetime
import time

class Icecream:
    def __init__(self):
        self.create_time = datetime.now()

if __name__ == "__main__":
    ice_1 = Icecream()
    time.sleep(3)
    ice_2 = Icecream()
    print(ice_1.create_time)
    print(ice_2.create_time)