import schedule
import time
from datetime import datetime
from scrapper import get_all_articles

def print_something():
    print("Hello at: " + str(datetime.now()))
    print(get_all_articles())


def main():
    schedule.every().day.at("10:00").do(print_something)
    schedule.every().day.at("10:01").do(print_something)
    schedule.every().day.at("10:02").do(print_something)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
