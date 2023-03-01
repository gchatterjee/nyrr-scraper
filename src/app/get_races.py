from typing import Dict, Union
from bs4 import BeautifulSoup

from race import Race


def get_field(soup: BeautifulSoup, field: str) -> Union[str, None]:
    result = soup.find(class_="index_listing__{}".format(field))
    if result is None:
        return None
    result = result.get_text().strip()
    return result if result != "" else None


def get_url(soup: BeautifulSoup) -> Union[str, None]:
    div = soup.find(class_="index_listing__title")
    if div is None:
        return None
    a = div.find("a")
    if a is None or not a.has_attr("href"):
        return None
    result = a["href"].strip()
    return result if result != "" else None


def source_to_race(soup: BeautifulSoup) -> Race:
    fields = ["date", "time", "title", "status", "location"]
    race = {}
    for field in fields:
        race[field] = get_field(soup, field)
    url = get_url(soup)
    return Race(
        race["title"], race["date"], race["time"], race["location"], race["status"], url
    )


def get_races(html: str) -> Dict[str, Race]:
    soup = BeautifulSoup(html, features="html.parser")
    races = map(source_to_race, soup.find_all(class_="index_listing"))
    result = {}
    for race in races:
        if race.title is not None:
            result[race.title] = race
    return result
