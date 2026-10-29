
import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


def assert_json_error(res, expected_status):
    """Check the status code and JSON error response."""
    assert res.status_code == expected_status, (
        f"Expected {expected_status}, got {res.status_code}: {res.text}"
    )
    body = res.json()
    assert isinstance(body, dict)
    assert isinstance(body.get("error"), str)
    assert body["error"] != ""


# Base choice: valid stars, integer type, existing pizza, own token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: values below 1 and above 5 must be rejected.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: decimal, string and missing stars must be rejected.
@pytest.mark.parametrize(
    "case, stars",
    [
        ("decimal", 3.5),
        ("string", "3"),
        ("missing", None),
    ],
    ids=["decimal", "string", "missing"]
)
def test_invalid_stars_type(api, auth, pizza_id, case, stars):
    new = {"pizza_id": pizza_id}

    if case != "missing":
        new["stars"] = stars

    res = api.post("/api/ratings", json=new, headers=auth)
    assert_json_error(res, 400)


# C3: rating with a nonexistent pizza ID must be rejected.
def test_nonexistent_pizza(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert_json_error(res, 400)


# C4: a request without an Authorization token is rejected.
def test_missing_token(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)

    assert_json_error(res, 401)


# C4: a token with an invalid length is rejected.
def test_invalid_token_length(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    bad_auth = {"Authorization": "token short"}

    res = api.post(
        "/api/ratings",
        json=new,
        headers=bad_auth
    )

    assert_json_error(res, 401)
