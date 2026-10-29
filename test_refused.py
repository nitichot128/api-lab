# Reject a username that is already registered.
def test_duplicate_username_is_refused(api):
    from conftest import log_in_new_user

    # Create a unique user, then register the same name again.
    # The fixture helper returns only an auth header,
    # so this test creates its own username directly.
    import uuid

    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}

    first = api.post("/api/users", json=user)
    assert first.status_code == 201

    second = api.post("/api/users", json=user)
    assert second.status_code == 400
    assert second.json() == {
        "error": "username already taken"
    }


# Reject login with the wrong password.
def test_wrong_password_is_refused(api):
    import uuid

    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}

    res = api.post("/api/users", json=user)
    assert res.status_code == 201

    wrong = {
        "username": name,
        "password": "WrongPassword"
    }
    res = api.post(
        "/api/users/token/login",
        json=wrong
    )
    assert res.status_code == 401
    assert res.json() == {
        "error": "authentication failed"
    }


# Reject registration with an empty username.
def test_empty_username_is_refused(api):
    user = {"username": "", "password": "Pizza-2026"}

    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {
        "error": "username field is empty"
    }