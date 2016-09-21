from food_network_wrapper import recipe_search, get_n_recipes, scrape_recipe


def main():
    rthumbnails = get_n_recipes("tacos")
    recipes = []
    for i in rthumbnails:
        print("Scraping ...")
        print(i.title)
        print(i.url)
        print(i.author)
        print(i.picture_url)
        print(i.total_time)
        print(i.rating)
        print(i.review_count)

        recipe = scrape_recipe(i.url)
        recipes.append(recipe)
        
    for i in recipes:
        print(i.title)
        print(i.author)
        print(i.picture_url)
        print(i.total_time)
        print(i.prep_time)
        print(i.cook_time)
        print(i.servings)
        print(i.level)
        print(i.ingredients)
        print(i.directions)
        print(i.categories)



if __name__ == "__main__":
    main()
