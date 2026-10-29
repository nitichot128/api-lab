# A new rating has its own ID, stars and pizza ID.
def test_create_rating(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 5}

    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201

    body = res.json()
    assert body["stars"] == 5
    assert body["pizza_id"] == pizza_id
    assert isinstance(body["id"], int)

# Read the existing rating by its ID.
def test_read_rating(api, auth, rating):
    res = api.get(
        f"/api/ratings/{rating['id']}",
        headers=auth
    )
    assert res.status_code == 200
    assert res.json() == rating


# Update the rating stars.
def test_update_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(
        path, json={"stars": 4}, headers=auth
    )
    assert res.status_code == 200
    assert res.json()["stars"] == 4


# Delete the rating and confirm it cannot be read.
def test_delete_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"

    res = api.delete(path, headers=auth)
    assert res.status_code == 204

    res = api.get(path, headers=auth)
    assert res.status_code == 404