import pytest

from audio_asset_manager.forms import AudioAssetForm, CollectionForm

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.parametrize("form_class", [CollectionForm, AudioAssetForm])
def test_form_requires_user_to_initialize(form_class):
    with pytest.raises(KeyError):
        form_class()
