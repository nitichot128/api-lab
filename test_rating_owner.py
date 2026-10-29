
# A different user must not read the owner's rating.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"

    res = api.get(path, headers=other_auth)
    print("Other user GET status:", res.status_code)

    assert 400 <= res.status_code <= 499

    # Owner must still be able to read the original rating.
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating


# A different user must not update the owner's rating.
def test_other_user_cannot_update(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"

    res = api.put(
        path,
        json={"stars": 5},
        headers=other_auth
    )
    print("Other user PUT status:", res.status_code)

    assert 400 <= res.status_code <= 499

    # The rating must remain unchanged.
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating


# A different user must not delete the owner's rating.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"

    res = api.delete(path, headers=other_auth)
    print("Other user DELETE status:", res.status_code)

    assert 400 <= res.status_code <= 499

    # The owner's rating must still exist.
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating
