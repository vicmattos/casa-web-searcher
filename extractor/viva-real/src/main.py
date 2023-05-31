import configparser
import csv
import os
import pathlib
import sys

import bs4
import requests


def main():
    parser = configparser.ConfigParser()
    parser.read("settings.cfg")
    for execution_name in parser.sections():
        config = parser[execution_name]
        data = extract_data(execution_name, config.get("url"))
        with open(f"data/{execution_name}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(data)


def extract_data(extraction_name: str, url: str) -> list:
    data = []
    html = fetch_html(url)
    soup = bs4.BeautifulSoup(html, features="html.parser")
    for div in soup.find_all(
        lambda tag: tag.get("id").isnumeric() if "id" in tag.attrs else False
    ):
        data.append(extract_values_from_div(div))
    return data


def fetch_html(url: str) -> str:
    resp = requests.get(url)
    return resp.text


def extract_values_from_div(div: bs4.element.Tag) -> tuple:
    title = div.find(class_="property-card__title").text.strip()
    address = div.find(class_="property-card__address").text.strip()
    area = div.find(class_="js-property-card-detail-area").text.strip()
    rooms = div.find(class_="property-card__detail-room").text.strip()
    bathrooms = div.find(class_="property-card__detail-bathroom").text.strip()
    garages = div.find(class_="property-card__detail-garage").text.strip()
    rent = div.find(class_="property-card__values").text.strip()
    return (title, address, area, rooms, bathrooms, garages, rent)


if __name__ == "__main__":
    os.chdir(pathlib.Path(sys.path[0]) / "..")
    main()
