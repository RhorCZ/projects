import sys
import csv
import requests
import os
from typing import Union
from bs4 import BeautifulSoup


# Process given arguments
def get_arguments():
    try:
        if not len(sys.argv) == 3:
            raise Exception("Wrong number of arguments! Expected two of them!")
        elif "https://volby.cz/pls/ps" not in sys.argv[1]:
            raise Exception("Invalid URL!")
        elif len(sys.argv[2]) <= 4 or not sys.argv[2].endswith(".csv"):
            raise Exception("Invalid filename!")
        return sys.argv[1], sys.argv[2]
    except Exception as ex:
        print(ex)
        print('Example: python electionsscraper.py "elections-url" "filename.csv"')
        exit(0)


# Make sure that filename is original
def process_filename(filename: str) -> str:
    new_filename = filename
    path, file = os.path.split(filename)
    original_filename = file
    index = 1
    while True:
        if os.path.exists(os.path.join(path, file)):
            # Rename
            file = original_filename.split(".")[0] + "(" + str(index) + ")" + ".csv"
            index += 1
            new_filename = os.path.join(path, file)
        else:
            break
    return new_filename


def get_villages(url: str) -> dict():
    try:
        village_dict = dict()
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        rows = soup.find_all('tr')

        def add_village(number: str, name: str, link):
            if link is None:
                return
            village_link = link.get("href")
            village_link = "/".join(url.split("/")[:-1]) + "/" + village_link
            village_dict[number] = dict()
            village_dict[number]["name"] = name
            village_dict[number]["link"] = village_link

        for tr in rows:
            columns = tr.find_all('td')
            if len(columns) >= 3:
                # Get correct link from new/old elections tables
                if len(columns) == 3 or len(columns) == 7:
                    add_village(columns[0].text.strip(), columns[1].text.strip(), columns[0].find('a'))
                    if len(columns) == 7:
                        add_village(columns[4].text.strip(), columns[5].text.strip(), columns[4].find('a'))
                else:
                    add_village(columns[0].text.strip(), columns[1].text.strip(), columns[2].find('a'))

        if village_dict is None:
            raise Exception("Failed to get villages from URL!")

        return village_dict

    except Exception as ex:
        print(ex)
        exit(0)


def get_election_data(villages: dict, header: list) -> Union[list, list]:
    csv_rows = list()
    csv_header = header

    for key, value in villages.items():
        try:
            row = [key, villages[key]["name"]]
            page = requests.get(villages[key]["link"])
            soup = BeautifulSoup(page.text, "html.parser")
            tables = soup.find_all("table")

            header_table = tables[0].find_all("tr")

            # Handle newer elections table
            if len(tables) == 3:
                main_table = tables[1].find_all("tr") + tables[2].find_all("tr")
            # Handle older elections table
            elif len(tables) == 2:
                main_table = tables[1].find_all("tr")
            else:
                raise Exception("Failed to retrieve data from", villages[key]["link"])

            row += process_header_table(header_table)
            results_row, candidates = process_main_table(main_table)
            row += results_row
            csv_rows.append(row)

            if not len(header) + len(candidates) == len(csv_header):
                csv_header = header + candidates

        except Exception as ex:
            print(ex)

    return csv_rows, csv_header


# Part of get_election_data
def process_header_table(rows):
    csv_row = list()
    for row in rows:
        columns = row.find_all("td")
        if columns is not None and len(columns) >= 7:
            csv_row = [columns[3].text.strip(), columns[4].text.strip(), columns[7].text.strip()]
            break
    return csv_row


# Part of get_election_data
def process_main_table(rows):
    csv_row = list()
    candidates = list()
    for row in rows:
        columns = row.find_all("td")
        if columns is not None:
            # Handle newer elections result table
            if len(columns) == 5:
                candidate_name = columns[1].text.strip()
                candidate_result = columns[2].text.strip()
                if not candidate_name == "-":
                    csv_row.append(candidate_result)
                    candidates.append(candidate_name)
            # Handle older elections result table
            elif len(columns) == 9:
                candidate_name = columns[1].text.strip()
                candidate_name2 = columns[6].text.strip()
                candidate_result = columns[2].text.strip()
                candidate_result2 = columns[7].text.strip()
                if not candidate_name == "":
                    csv_row.append(candidate_result)
                    candidates.append(candidate_name)
                if not candidate_name2 == "":
                    csv_row.append(candidate_result2)
                    candidates.append(candidate_name2)

    return csv_row, candidates


def write_csv(file: str, header: list, rows: list):
    try:
        with open(file, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
    except Exception:
        print("Error occured:\n", sys.exc_info()[0])
        exit(0)


def main():
    url, file = get_arguments()
    file = process_filename(file)
    villages = get_villages(url)
    initial_header = ["Kod obce", "Nazev obce", "Volici v seznamu", "Vydane obalky", "Platne hlasy"]
    csv_rows, csv_header = get_election_data(villages, initial_header)
    write_csv(file, csv_header, csv_rows)
    print("Done")


if __name__ == "__main__":
    main()
