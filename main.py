from scrape import scrape_data
from process import process_data
import json
def main():
    save_location = scrape_data()
    # save_location = "data/scrape/data_2024-06-21_20-20-41.json"
    print("scrape done")
    print("Press enter to continue.")
    input()  # This will pause the script until the user presses enter
    print("The program will now proceed.")
    with open(save_location) as f:
        activities = json.load(f)
    # process_data(activities[:2])
    process_data(activities)


if __name__ == "__main__":
    main()
