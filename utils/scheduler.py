import schedule
import time
from datetime import datetime

def print_something():
    print("Hello at: " + str(datetime.now()))


def main():
    schedule.every().day.at("11:27").do(print_something)
    schedule.every().day.at("11:29").do(print_something)
    schedule.every().day.at("11:31").do(print_something)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
