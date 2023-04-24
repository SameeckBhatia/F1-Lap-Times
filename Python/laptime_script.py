import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

# creating dictionaries to associate round numbers to attributes
driver_team_dict = {"alonso": "Aston Martin", "hamilton": "Mercedes",
                    "leclerc": "Ferrari", "perez": "Red Bull",
                    "russell": "Mercedes", "sainz": "Ferrari",
                    "stroll": "Aston Martin", "max_verstappen": "Red Bull"}

# creating a dictionary with information by round
round_dict = {1: ["Bahrain", 57], 2: ["Saudi Arabia", 50], 3: ["Australia", 58],
              4: ["Azerbaijan", 51], 5: ["Miami", 57],
              6: ["Emilia Romagna", 63], 7: ["Monaco", 78]}

# initializing gp information
round_num = 0
df = pd.read_csv("data.csv")
for rd in range(23):
    if not rd + 1 in df["round"].tolist():
        round_num = rd + 1
        break

gp = round_dict[round_num][0]
laps = round_dict[round_num][1]

# opening data file for appending
with open('data.csv', mode='a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, lineterminator="\n")

    # running a loop through each driver
    for driver in driver_team_dict:

        # running a loop through each lap
        for i in range(laps):

            # using the 'ergast' API to gather lap time information
            url = 'https://ergast.com/api/f1/2023/' + str(
                round_num) + '/drivers/' + driver + '/laps/' + str(i + 1)
            response = requests.get(url)

            # parsing through XML document
            soup = BeautifulSoup(response.text, 'xml')

            # checking if timing data is None
            if soup.find('Timing') is None:
                break

            # converting time format from <mm:ss.sss> to <ss.sss>
            comma_index = soup.find('Timing')['time'].index(":")
            minutes = float(soup.find('Timing')['time'][0])
            seconds = float(soup.find('Timing')['time'][comma_index + 1:])
            time = round(seconds + minutes * 60, 3)

            # collecting position information
            pos = int(soup.find('Timing')['position'])

            # assigning driver codes from driver names
            driver_code = driver[:3].upper()

            # creating unique driver code for Max Verstappen
            if driver_code == "MAX":
                driver_code = "VER"

            # writing row to file
            csv_writer.writerow(
                [driver_code, i + 1, pos, time, "", driver_team_dict[driver],
                 gp, round_num])
