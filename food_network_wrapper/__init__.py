import requests
from bs4 import BeautifulSoup
import json
import re

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


def _parse_recipe_list(recipe_thumbnails):
    articles = recipe_thumbnails.find_all("article", {"class": "recipe"})
    return list(map(_parse_recipe_thumbnail, articles))


def get_n_recipes(query, n=10, sortby="Best Match"):
    calls = n / 10
    page = 1
    rthumbnails = []
    while calls >= 0:
        curr_rthumbnails = recipe_search(query, page, sortby)
        if len(curr_rthumbnails) == 0 or len(rthumbnails) >= n:
            break
        rthumbnails.extend(curr_rthumbnails)
        page += 1
        calls -= 1

    return rthumbnails[:n]


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
    recipe_thumbnails = soup.find("ul", {"class": "slat feed"})
    if recipe_thumbnails is None:
        return []
    else:
        return _parse_recipe_list(recipe_thumbnails)


def _parse_recipe(recipe_html):
    try:
        title = recipe_html.find("h1", itemprop="name").text
    except AttributeError:
        title = ""
    try:
        for span in recipe_html.findAll("span", attrs={'class':'o-Attribution__a-Author--Prefix'}):
            for namespan in span.findAll("span", attrs={'class':'o-Attribution__a-Name'}):
                author = namespan.find("a").contents[0]
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
        tot_hrs = tot_mins = total_minutes = prep_hrs = prep_mins = prep_minutes = int()
        get_tot_matches = re.match('((\d+) hr )?((\d+) min)?', total_time)
        get_prep_matches = re.match('((\d+) hr )?((\d+) min)?', prep_time)
        try:
            tot_hrs = int(get_tot_matches.group(2))
        except (AttributeError, ValueError):
            tot_hrs = int(0)
            print("Total regex fallthrough")
        try:
            tot_mins = int(get_tot_matches.group(4))
        except (AttributeError, ValueError):
            tot_mins = int(0)
        total_minutes = (tot_hrs * 60) + tot_mins
        try:
            prep_hrs = int(get_prep_matches.group(2))
        except (AttributeError, ValueError):
            prep_hrs = int(0)
        try:
            prep_mins = int(get_prep_matches.group(4))
        except (AttributeError, ValueError):
            prep_mins = int(0)
        prep_minutes = (prep_hrs * 60) + prep_mins
        cook_time_minutes = total_minutes - prep_minutes
        cook_time_mins = int(cook_time_minutes % 60)
        cook_time_hrs = int(cook_time_minutes / 60)
        if cook_time_hrs > 0:
            cook_time = str(cook_time_hrs) + " hr " + str(cook_time_minutes) + " min"
        else:
            cook_time = str(cook_time_minutes) + " min"
        print(prep_hrs, prep_minutes, tot_hrs, total_minutes, cook_time_hrs,
              cook_time_minutes, cook_time_mins)
    except IndexError:
        cook_time = ""
    try:
        picture_url = recipe_html.find("div", attrs={'class': 'o-AssetMultiMedia__m-MediaWrap'}).find("img").attrs['src']
    except AttributeError:
        picture_url = ""
    try:
        for section in recipe_html.findAll("section", attrs={'class': 'o-RecipeInfo o-Level'}):
            level = section.find("dd", attrs={'class': 'o-RecipeInfo__a-Description'}).string.strip()
    except AttributeError:
        level = ""
    try:
        servings = difficulty[0].text
    except IndexError:
        servings = ""
    try:
        ings_div = recipe_html.find("div", attrs={'class': "o-Ingredients__m-Body"})
        ingredients = list(map(lambda x: x.text, ings_div.find_all("li", attrs={'class': 'o-Ingredients__a-ListItem'})))
        ingredients = [i.replace('\n','') for i in ingredients]
    except AttributeError:
        ingredients = []
    try:
        for desc_div in recipe_html.findAll("div", attrs={'class': 'o-Method__m-Body'}):
            directions = list(map(lambda x: x.text, desc_div.find_all("p")))
            directions = [d.replace('\n','') for d in directions]
            directions = [d.strip() for d in directions]
    except AttributeError:
        directions = []
    try:
        categories = []
        for tag in recipe_html.findAll("a", attrs={'class': 'o-Capsule__a-Tag a-Tag'}):
            categories.append(tag.text)
        if not categories:
            raise ValueError('Categories list is empty')
    except (ValueError, UnboundLocalError) as ex:
        categories = []
        print("Categories parsing threw error: ", ex)


    return Recipe(title, author, picture_url, total_time, prep_time, cook_time, servings, level, ingredients, directions, categories)


def scrape_recipe(url):
    """
    parameter: url to Food Network recipe
    return: Recipe object
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return _parse_recipe(soup)
