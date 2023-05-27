import configparser
import os
import pathlib
import sys

import bs4
import requests


def main():
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    for key in config["URLs.viva-real"]:
        html = fetch_html(config["URLs.viva-real"][key])
        soup = bs4.BeautifulSoup(html, features="html.parser")
        for div in soup.find_all(lambda tag: tag.get('id').isnumeric() if 'id' in tag.attrs else False):
            print(extract_values_from_div(div))


def fetch_html(url: str) -> str:
    resp = requests.get(url)
    return resp.text


def extract_values_from_div(div: bs4.element.Tag) -> tuple:
    title = div.find(class_='property-card__title').text.strip()
    address = div.find(class_='property-card__address').text.strip()
    area = div.find(class_='js-property-card-detail-area').text.strip()
    rooms = div.find(class_='property-card__detail-room').text.strip()
    bathrooms = div.find(class_='property-card__detail-bathroom').text.strip()
    garages = div.find(class_='property-card__detail-garage').text.strip()
    rent = div.find(class_='property-card__values').text.strip()
    return (title, address, area, rooms, bathrooms, garages, rent)


if __name__ == "__main__":
    os.chdir(pathlib.Path(sys.path[0])/'..')
    main()
