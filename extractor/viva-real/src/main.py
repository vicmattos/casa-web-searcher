import os
import pathlib
import sys

import bs4


def main():
    with open("butanta-4000-3quartos.html") as fp:
        soup = bs4.BeautifulSoup(fp, features="html.parser")
    for div in soup.find_all(lambda tag: tag.get('id').isnumeric() if 'id' in tag.attrs else False):
        print(extract_values_from_div(div))


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
    os.chdir(pathlib.Path(sys.path[0])/'..'/'data')
    main()
