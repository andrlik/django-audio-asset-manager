from typing import List

import pytest
from django.contrib.auth import get_user_model

from audio_asset_manager.models import Artist, AssetSource, AudioAsset, Collection
from tests.factories.user import UserFactory

User = get_user_model()


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def user2() -> User:
    return UserFactory()


@pytest.fixture
def user_created_assets(user) -> List[AudioAsset]:
    """
    Generates basic existing data for a catalog that of
    assets for use in testing.
    """
    assets: List[AudioAsset] = []
    js = Artist.objects.create(name="John Smith", owner=user)
    jd = Artist.objects.create(name="Jane Doe", owner=user)
    db = Artist.objects.create(name="Sk8F4N", owner=user)
    asdb = AssetSource.objects.create(
        name="DB Studios", source_credit_text="/ via DB Studios", owner=user
    )
    asas = AssetSource.objects.create(
        name="Adobe Stock", source_credit_text="/ via Adobe Stock", owner=user
    )
    emoji = Artist.objects.create(name="🥰", owner=user)
    col = Collection.objects.create(title="SFX Pack 40", album_artist=db, owner=user)
    assets.append(
        AudioAsset.objects.create(
            title="Creepy Scream",
            asset_type=AudioAsset.AssetTypes.SFX,
            artist=db,
            collection=col,
            source=asdb,
            owner=user,
        )
    )
    assets.append(
        AudioAsset.objects.create(
            title="Man Yelling",
            asset_type=AudioAsset.AssetTypes.SFX,
            artist=db,
            collection=col,
            source=asdb,
            owner=user,
        )
    )
    assets.append(
        AudioAsset.objects.create(
            title="Footsteps in Leaves",
            asset_type=AudioAsset.AssetTypes.SFX,
            artist=db,
            collection=col,
            source=asdb,
            owner=user,
        )
    )
    assets.append(
        AudioAsset.objects.create(
            title="Anxiety Atmos",
            asset_type=AudioAsset.AssetTypes.MUSIC,
            artist=js,
            source=asas,
            owner=user,
        )
    )
    assets.append(
        AudioAsset.objects.create(
            title="March of the Heroes",
            asset_type=AudioAsset.AssetTypes.MUSIC,
            artist=jd,
            source=asas,
            owner=user,
        )
    )
    assets.append(
        AudioAsset.objects.create(
            title="Idle Hero Theme (Dubstep Remix)",
            asset_type=AudioAsset.AssetTypes.MUSIC,
            artist=emoji,
            source=asas,
            owner=user,
        )
    )
    yield assets
    for asset in assets:
        asset.delete()
    col.delete()
    asdb.delete()
    asas.delete()
    for artist in [js, jd, emoji, db]:
        artist.delete()
