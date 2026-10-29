import requests

SITE = "https://quickpizza.grafana.com"
AUTH = {"Authorization": "token abcdef0123456789"}
VEGETARIAN = {"mustBeVegetarian": True}

# Vegetarian pizza must use vegetarian ingredients.
def test_vegetarian_pizza():
    res = requests.post(
        SITE + "/api/pizza",
        json=VEGETARIAN,
        headers=AUTH
    )
    assert res.status_code == 200

    body = res.json()
    assert body["pizza"]["name"] != ""

    for ingredient in body["pizza"]["ingredients"]:
        assert ingredient["vegetarian"] is True, ingredient["name"]


# An unauthenticated pizza request must be refused.
def test_pizza_without_token_is_refused():
    res = requests.post(
        SITE + "/api/pizza",
        json=VEGETARIAN
    )
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}