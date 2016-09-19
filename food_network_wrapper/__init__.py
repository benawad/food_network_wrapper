import requests
from bs4 import BeautifulSoup
import json

from .RThumbnail import RThumbnail


def _parse_recipe_thumbnail(recipe_thumbnail):
    h6 = recipe_thumbnail.find("h6")
    title = h6.text.strip()
    url = h6.find("a").attrs['href']

    try:
        author = recipe_thumbnail.find("p").find("a").text.strip()
    except AttributeError:
        author = ""

    reviews_json = recipe_thumbnail.find("a", class_="community-rating-stars").attrs["data-rating"]
    reviews_d = json.loads(reviews_json)
    rating = reviews_d['ratingaverage']
    review_count = reviews_d['reviewsnumber']

    total_time = recipe_thumbnail.find("dl", class_="flat").find("dd").text

    try:
        picture_url = recipe_thumbnail.find("div", class_="pull-right").find("img").attrs['src']
    except AttributeError:
        picture_url = ""

    return RThumbnail(title, url, author, picture_url, total_time, rating, review_count)


def _parse_recipe_list(recipe_thumbails):
    articles = recipe_thumbails.find_all("article", {"class": "recipe"})
    return list(map(_parse_recipe_thumbnail, articles))

def recipe_search(query, page=1):
    """
    max of 10 recipes per request
    return: RThumbnail list
    """
    url = "http://www.foodnetwork.com/search/search-results.recipes.html?searchTerm=%s&page=%s&form=global&_charset_=UTF-8" % (query, page)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    recipe_thumbails = soup.find("ul", {"class": "slat feed"})
    if recipe_thumbails is None:
        return []
    else:
        return _parse_recipe_list(recipe_thumbails)


