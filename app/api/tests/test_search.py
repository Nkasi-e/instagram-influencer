def test_search_route(client, test_profile):
    res = client.get("/search/")
    assert res.status_code == 200
    assert res.json() == list(res.json())
    assert len(res.json()) == len(test_profile)


def test_search_query(client, test_profile):
    res = client.get("/search?text=software&max_followers=10")
    profile = res.json()[0]
    assert profile["username"] == "snipes"
    assert profile["followers"] == 10
    assert profile["bio"] == "Software Engineer"
    assert res.status_code == 200
