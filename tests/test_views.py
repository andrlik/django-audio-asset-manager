import pytest
from django.urls import reverse

from audio_asset_manager.models import Artist, AssetSource, AudioAsset, Collection

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


def test_detail_views_require_login(
    client, django_assert_max_num_queries, user_created_assets
):
    test_asset = user_created_assets[0]
    test_artist = test_asset.artist
    test_collection = test_asset.collection
    test_source = test_asset.source
    with django_assert_max_num_queries(50):
        response = client.get(
            reverse("audio_asset_manager:asset-detail", kwargs={"pk": test_asset.id})
        )
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]
    with django_assert_max_num_queries(50):
        response = client.get(
            reverse("audio_asset_manager:artist-detail", kwargs={"pk": test_artist.id})
        )
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]
    with django_assert_max_num_queries(50):
        response = client.get(
            reverse(
                "audio_asset_manager:collection-detail",
                kwargs={"pk": test_collection.id},
            )
        )
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]
    with django_assert_max_num_queries(50):
        response = client.get(
            reverse("audio_asset_manager:source-detail", kwargs={"pk": test_source.id})
        )
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


@pytest.mark.parametrize("view_name", ["asset-detail", "asset-update", "asset-delete"])
def test_wrong_user_not_authorized_all_asset_views(
    client, django_assert_max_num_queries, user2, user_created_assets, view_name
):
    asset = user_created_assets[0]
    url = reverse(f"audio_asset_manager:{view_name}", kwargs={"pk": asset.id})
    client.force_login(user2)
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 403
    with django_assert_max_num_queries(50):
        response = client.post(url, data={})
    assert response.status_code == 403
    if "delete" in view_name:
        assert AudioAsset.objects.get(pk=asset.pk)


@pytest.mark.parametrize(
    "view_name", ["source-detail", "source-update", "source-delete"]
)
def test_wrong_user_not_authorized_all_assetsource_views(
    client, django_assert_max_num_queries, user2, user_created_assets, view_name
):
    source = user_created_assets[0].source
    url = reverse(f"audio_asset_manager:{view_name}", kwargs={"pk": source.id})
    client.force_login(user2)
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 403
    with django_assert_max_num_queries(50):
        response = client.post(url, data={})
    assert response.status_code == 403
    if "delete" in view_name:
        assert AssetSource.objects.get(pk=source.id)


@pytest.mark.parametrize(
    "view_name", ["artist-detail", "artist-update", "artist-delete"]
)
def test_wrong_user_not_authorized_all_artist_views(
    client, django_assert_max_num_queries, user2, user_created_assets, view_name
):
    artist = user_created_assets[0].artist
    url = reverse(f"audio_asset_manager:{view_name}", kwargs={"pk": artist.id})
    client.force_login(user2)
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 403
    with django_assert_max_num_queries(50):
        response = client.post(url, data={})
    assert response.status_code == 403
    assert Artist.objects.get(pk=artist.id)


@pytest.mark.parametrize(
    "view_name", ["collection-detail", "collection-update", "collection-delete"]
)
def test_wrong_user_not_authorized_all_collection_views(
    client, django_assert_max_num_queries, user2, user_created_assets, view_name
):
    col = user_created_assets[0].collection
    url = reverse(f"audio_asset_manager:{view_name}", kwargs={"pk": col.id})
    client.force_login(user2)
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 403
    with django_assert_max_num_queries(50):
        response = client.post(url, data={})
    assert response.status_code == 403
    assert Collection.objects.get(pk=col.id)


@pytest.mark.parametrize("view_name", ["asset-detail", "asset-update", "asset-delete"])
def test_authorized_user_get_asset_views(
    client, django_assert_max_num_queries, user_created_assets, view_name
):
    asset = user_created_assets[0]
    client.force_login(asset.owner)
    url = reverse(f"audio_asset_manager:{view_name}", kwargs={"pk": asset.id})
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 200
