import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.parametrize("viewname", ["source-list", "artist-list", "asset-list"])
def test_list_views_require_login(client, viewname):
    """
    Ensure that all our list views require login.
    """
    response = client.get(reverse(f"audio_asset_manager:{viewname}"))
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


@pytest.mark.parametrize(
    "viewname,expected_length",
    [("source-list", 2), ("artist-list", 4), ("asset-list", 6)],
)
def test_list_views_include_correct_data_for_user(
    client,
    django_assert_max_num_queries,
    user,
    user_created_assets,
    viewname,
    expected_length,
):
    url = reverse(f"audio_asset_manager:{viewname}")
    client.force_login(user)
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["object_list"]) == expected_length
    for obj in response.context["object_list"]:
        assert obj.owner == user


@pytest.mark.parametrize("viewname", ["source-list", "artist-list", "asset-list"])
def test_other_user_does_not_see_records(
    client, django_assert_max_num_queries, user2, user_created_assets, viewname
):
    url = reverse(f"audio_asset_manager:{viewname}")
    client.force_login(user2)
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["object_list"]) == 0
