# importing required libraries
import os.path
import requests
import threading
from bs4 import *
from pandas import *
from typing import *

# dataframe header row
header_dict = {
    "round": [], "grand_prix": [], "constructor": [],
    "driver": [], "lap": [], "time": []
}

# driver-constructor association
cons_dict = {
    "alonso": "Aston Martin", "hamilton": "Mercedes",
    "leclerc": "Ferrari", "perez": "Red Bull",
    "russell": "Mercedes", "sainz": "Ferrari",
    "stroll": "Aston Martin", "max_verstappen": "Red Bull"
}

# round number information
round_dict = {
    1: ["Bahrain", 57], 2: ["Saudi Arabia", 50], 3: ["Australia", 58],
    4: ["Azerbaijan", 51], 5: ["Miami", 57], 6: ["Monaco", 78],
    7: ["Spain", 66], 8: ["Canada", 70], 9: ["Austria", 71]
}

# list to store all driver dataframes
df_list = []


# checking whether driver data file exists
def check_existing_file() -> set:
    round_dict_set = set(round_dict.keys())
    file_data = read_csv("python/data.csv")
    if os.path.isfile("python/data.csv") and len(file_data) > 0:
        file_round_set = set(file_data["round"])
        difference_set = round_dict_set.difference(file_round_set)
        # returning difference of round numbers
        return difference_set
    else:
        # returning all of the round numbers
        return round_dict_set


# scraping driver data and storing values in seperate dataframes
def collect_and_structure(driver: str) -> None:
    df = DataFrame(data=header_dict)
    # running through round numbers
    for i in check_existing_file():
        # running through the laps
        for j in range(round_dict[i][1]):
            lap = j + 1
            grand_prix = round_dict[i][0]
            round_num = i

            # setting API endpoints and parsing xml from them
            url = f"https://ergast.com/api/f1/2023/{round_num}/drivers/{driver}/laps/{lap}"

            response = requests.get(url)
            soup = BeautifulSoup(response.text, "xml").find("Timing")

            # cleaning values if data has been queried
            if soup is not None:
                minutes = float(soup["time"].split(":")[0])
                seconds = float(soup["time"].split(":")[1])

                df.loc[len(df)] = [round_num, grand_prix, cons_dict[driver],
                                   driver[:3].upper(), lap, round(minutes * 60 + seconds, 3)]

    df_list.append(df)


# creating and joining threads
def multithreading() -> None:
    t1 = threading.Thread(target=collect_and_structure, args=("alonso",))
    t2 = threading.Thread(target=collect_and_structure, args=("hamilton",))
    t3 = threading.Thread(target=collect_and_structure, args=("leclerc",))
    t4 = threading.Thread(target=collect_and_structure, args=("russell",))
    t5 = threading.Thread(target=collect_and_structure, args=("perez",))
    t6 = threading.Thread(target=collect_and_structure, args=("sainz",))
    t7 = threading.Thread(target=collect_and_structure, args=("stroll",))
    t8 = threading.Thread(target=collect_and_structure,
                          args=("max_verstappen",))

    t1.start(), t2.start(), t3.start(), t4.start(),
    t5.start(), t6.start(), t7.start(), t8.start()

    t1.join(), t2.join(), t3.join(), t4.join(),
    t5.join(), t6.join(), t7.join(), t8.join()


# merging dataframes with file data (if it exists) and writing to CSV
def merge_and_write(input_lst: list) -> None:
    new_lst = input_lst
    if os.path.isfile("python/data.csv"):
        new_lst.insert(0, read_csv("python/data.csv"))

    df_export = concat(new_lst)
    df_export.to_csv("python/data.csv", index=False)


if __name__ == "__main__":
    multithreading()
    merge_and_write(df_list)
