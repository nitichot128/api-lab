import requests

SITE = "https://quickpizza.grafana.com"

# The list of names should contain Margherita.
def test_names_are_listed():
    res = requests.get(SITE + "/api/names")
    assert res.status_code == 200
    assert "Margherita" in res.json()["names"]