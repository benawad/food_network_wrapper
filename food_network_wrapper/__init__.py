import requests
from bs4 import BeautifulSoup
import json

from .RThumbnail import RThumbnail
from .Recipe import Recipe


base_url = "http://www.foodnetwork.com"


def _parse_recipe_thumbnail(recipe_thumbnail):
    try:
        h6 = recipe_thumbnail.find("h6")
        title = h6.text.strip()
        url = base_url + h6.find("a").attrs['href']
    except AttributeError:
        title = ""
        url = ""
    
    

    try:
        author = recipe_thumbnail.find("p").find("a").text.strip()
    except AttributeError:
        author = ""

    try:
        reviews_json = recipe_thumbnail.find("a", class_="community-rating-stars").attrs["data-rating"]
        reviews_d = json.loads(reviews_json)
        rating = reviews_d['ratingaverage']
        review_count = reviews_d['reviewsnumber']
    except AttributeError:
        rating = ""
        review_count = ""

    try:
        total_time = recipe_thumbnail.find("dl", class_="flat").find("dd").text
    except AttributeError:
        total_time = ""

    try:
        picture_url = recipe_thumbnail.find("div", class_="pull-right").find("img").attrs['src']
    except AttributeError:
        picture_url = ""

    return RThumbnail(title, url, author, picture_url, total_time, rating, review_count)


def _parse_recipe_list(recipe_thumbails):
    articles = recipe_thumbails.find_all("article", {"class": "recipe"})
    return list(map(_parse_recipe_thumbnail, articles))

def recipe_search(query, page=1, sortby="Best Match"):
    """
    max of 10 recipes per request
    return: RThumbnail list
    """
    url = "http://www.foodnetwork.com/search/search-results.recipes.html?searchTerm=%s&page=%s&form=global&_charset_=UTF-8" % (query, page)
    if sortby == "rating" or sortby == "popular":
        url += "&sortBy=" + sortby
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    recipe_thumbails = soup.find("ul", {"class": "slat feed"})
    if recipe_thumbails is None:
        return []
    else:
        return _parse_recipe_list(recipe_thumbails)


def _parse_recipe(recipe_html):
    try:
        title = recipe_html.find("h1", itemprop="name").text
    except AttributeError:
        title = ""
    try:
        author = recipe_html.find("p", class_="copyright").text.split('of')[1].strip()
    except (AttributeError, IndexError):
        author = ""

    try:
        times = recipe_html.find("div", class_="cooking-times").find_all("dd")
    except AttributeError:
        times = []
    try:
        total_time = times[0].text
    except IndexError:
        total_time = ""
    try:
        prep_time = times[1].text
    except IndexError:
        prep_time = ""
    try:
        cook_time = times[2].text
    except IndexError:
        cook_time = ""
    try:
        picture_url = recipe_html.find("a", href="#lightbox-recipe-image").find("img").attrs['src']
    except AttributeError:
        picture_url = ""
    try:
        difficulty = recipe_html.find("div", class_="difficulty").find_all('dd')
    except AttributeError:
        difficulty = []
    try:
        servings = difficulty[0].text
    except IndexError:
        servings = ""
    try:
        level = difficulty[1].text
    except IndexError:
        level = ""
    try:
        ings_div = recipe_html.find("div", class_="ingredients")
        ingredients = list(map(lambda x: x.text, ings_div.find_all("li", itemprop="ingredients")))
    except AttributeError:
        ingredients = []
    try:
        desc_ul = recipe_html.find("ul", class_="recipe-directions-list").find_all("li")
        directions = list(map(lambda x: x.text, desc_ul))
    except AttributeError:
        directions = []
    try:
        categories = list(map(lambda x: x.text, recipe_html.find("ul", class_="categories").find_all("li", itemprop="recipeCategory")))
    except AttributeError:
        categories = []

    return Recipe(title, author, picture_url, total_time, prep_time, cook_time, servings, level, ingredients, directions, categories)


def scrape_recipe(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return _parse_recipe(soup)
