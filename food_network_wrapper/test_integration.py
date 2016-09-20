from food_network_wrapper import recipe_search, scrape_recipe, base_url

def test_search_and_scrape():
    page = 1
    while True:
        rthumbnails = recipe_search("banana", page)
        if len(rthumbnails) == 0 or page > 1:
            break
        for i in rthumbnails:
            assert scrape_recipe(base_url + i.url)
        page += 1
