from food_network_wrapper import recipe_search


def test_not_empty():
    assert len(recipe_search("apple"))


def test_empty():
    assert recipe_search("ajslkdgajslkg") == []
    assert recipe_search("apple", 1000000000000) == []
    assert recipe_search("apple", -1) == []


def test_accurate():
    query = "Pan-Seared Salmon with Kale and Apple Salad"
    results = recipe_search(query)
    rt = results[0]
    assert rt.title == query
    assert rt.rating == "5.0"
    assert rt.review_count == "12"
    assert rt.total_time == "40 min"
    assert rt.url == "http://www.foodnetwork.com/recipes/food-network-kitchens/pan-seared-salmon-with-kale-and-apple-salad-recipe.html"
    assert rt.picture_url == "http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2013/11/25/0/FNK_pan-seared-salmon-with-kale-apple-salad_s4x3.jpg.rend.sni5col.jpeg"


def test_sorting():
    results = recipe_search("bacon")
    r1 = results[0]
    assert r1.title == "Roast Bacon"
    assert r1.author == "Ina Garten"

    results = recipe_search("bacon", sortby="rating")
    r1 = results[0]
    assert r1.title == "Cocoa-Rubbed Steak With Bacon-Whiskey Gravy"
    assert r1.author == "Food Network Kitchen"

    results = recipe_search("bacon", sortby="popular")
    r1 = results[0]
    assert r1.title == "Corn and Cheese Chowder"
    assert r1.author == "Ree Drummond"

