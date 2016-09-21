from food_network_wrapper import get_n_recipes

def test_gets_n():
    assert len(get_n_recipes("almond", 0)) == 0
    assert len(get_n_recipes("almond", 1)) == 1
    assert len(get_n_recipes("almond", 10)) == 10
    assert len(get_n_recipes("almond", 14)) == 14
    assert len(get_n_recipes("almond", 20)) == 20
