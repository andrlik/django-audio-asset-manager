from django import forms

from .models import Artist, AssetSource, AudioAsset, Collection


class AudioAssetForm(forms.ModelForm):
    """
    A form that restricts the artists, collections, and sources to
    objects owned by the user.
    """

    user = None
    artist = forms.ModelChoiceField(queryset=Artist.objects.filter(owner=user))
    collection = forms.ModelChoiceField(queryset=Collection.objects.filter(owner=user))
    source = forms.ModelChoiceField(queryset=AssetSource.objects.filter(owner=user))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user is None:
            raise KeyError("A user must be defined to invoke this form.!")

    class Meta:
        model = AudioAsset
        fields = [
            "asset_type",
            "title",
            "artist",
            "collection",
            "source",
            "filename",
            "credit_link",
            "explicit_credit_required",
            "duration",
            "bpm",
            "loudness",
            "tags",
        ]


class CollectionForm(forms.ModelForm):
    """
    A form for collections that limits the artist definition to ones
    owned by the current user.
    """

    user = None
    album_artist = forms.ModelChoiceField(queryset=Artist.objects.filter(owner=user))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user is None:
            raise KeyError("A user must be defined to invoke this form.!")

    class Meta:
        model = Collection
        fields = ["title", "album_artist"]
