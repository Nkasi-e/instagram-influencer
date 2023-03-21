from app.api.schema import profile
import pytest


@pytest.mark.parametrize(
    "username, followers, bio",
    [
        ("camila", 100, "I am a web developer"),
        ("johnDOe", 250, "I am a devOps engineer"),
    ],
)
def test_create_profile(authorized_user, username, bio, followers):
    profile_data = {"username": username, "followers": followers, "bio": bio}
    res = authorized_user.post("/profile/", json=profile_data)
    created_profile = profile.ProfileResponseSchema(**res.json())
    assert created_profile.username == username
    assert created_profile.followers == followers
    assert created_profile.bio == bio
    assert res.status_code == 201


def test_default_bio_to_null(authorized_user):
    profile_data = {"username": "testusername", "followers": 20}
    res = authorized_user.post("/profile/", json=profile_data)
    created_profile = profile.ProfileResponseSchema(**res.json())
    assert created_profile.username == "testusername"
    assert created_profile.followers == 20
    assert created_profile.bio == None
    assert res.status_code == 201


def test_unauthenticated_user_cannot_create_profile(client):
    profile_data = {"username": "testusername", "followers": 20}
    res = client.post("/profile/", json=profile_data)
    assert res.status_code == 401
    assert res.json()["detail"] == "Not authenticated"


def test_user_to_create_multiple_profile(authorized_user, test_profile):
    profile_data = {"username": "duplicateProfile", "followers": 30}
    res = authorized_user.post("/profile/", json=profile_data)
    assert res.status_code == 403
    assert res.json()["detail"] == f"Users cannot have more than one profile"
