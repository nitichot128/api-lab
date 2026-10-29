
import pytest


# Boundary values: invalid updates must not modify saved stars.
@pytest.mark.parametrize(
    "stars, expected_status",
    [
        (0, 400),
        (1, 200),
        (5, 200),
        (6, 400),
    ]
)
def test_update_rating_boundary(
    api, auth, rating, stars, expected_status
):
    path = f"/api/ratings/{rating['id']}"

    res = api.put(
        path,
        json={"stars": stars},
        headers=auth
    )

    assert res.status_code == expected_status

    if expected_status == 200:
        assert res.json()["stars"] == stars
    else:
        assert "error" in res.json()

    # Read the rating again to verify persistence.
    read = api.get(path, headers=auth)
    assert read.status_code == 200

    if expected_status == 200:
        assert read.json()["stars"] == stars
    else:
        assert read.json()["stars"] == rating["stars"]
