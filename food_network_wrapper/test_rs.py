from food_network_wrapper import rs


def test_not_empty():
    assert len(rs("apple"))


def test_empty():
    assert rs("ajslkdgajslkg") == []
    assert rs("apple", 1000000000000) == []
    assert rs("apple", -1) == []


def test_accurate():
    query = "Pan-Seared Salmon with Kale and Apple Salad"
    results = rs(query)
    rt = results[0]
    assert rt.title == query
    assert rt.rating == "5.0"
    assert rt.review_count == "12"
    assert rt.total_time == "40 min"
    assert rt.url == "/recipes/food-network-kitchens/pan-seared-salmon-with-kale-and-apple-salad-recipe.html"
    assert rt.picture_url == "http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2013/11/25/0/FNK_pan-seared-salmon-with-kale-apple-salad_s4x3.jpg.rend.sni5col.jpeg"
