import pytest

# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize(
    "excluded",
    [
        [],                       # Exclude 0 tools
        ["Knife"],                # Exclude 1 tool
        ["Scissors"],             # Exclude 1 tool
        ["Knife", "Scissors"],     # Exclude 2 tools
    ]
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)

    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Defect 1: Excluding all tools causes HTTP 500.
@pytest.mark.xfail(
    reason="Defect 1: Excluding all tools returns HTTP 500 instead of 400",
    strict=True
)
def test_all_tools_excluded_returns_client_error(api, auth):
    body = {
        "excludedTools": [
            "Knife",
            "Pizza cutter",
            "Scissors"
        ]
    }

    res = api.post("/api/pizza", json=body, headers=auth)

    assert res.status_code == 400
    assert res.headers["Content-Type"].startswith("application/json")
    assert isinstance(res.json().get("error"), str)
    assert res.json()["error"] != ""