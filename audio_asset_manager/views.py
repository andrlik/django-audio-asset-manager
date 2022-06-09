# Put your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from rules.contrib.views import AutoPermissionRequiredMixin

from .forms import AudioAssetForm, CollectionForm
from .models import Artist, AssetSource, AudioAsset, Collection


# Asset Source Views
class AssetSourceListView(LoginRequiredMixin, generic.ListView):
    """
    See a list of your AssetSource objects.
    """

    model = AssetSource
    paginate_by = 25
    ordering = ["name"]
    context_object_name = "sources"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise KeyError("A user needs to be logged in to access this page!")
        return self.model.objects.filter(owner=self.request.user)


class AssetSourceCreateView(LoginRequiredMixin, generic.edit.CreateView):
    """
    Create a new asset source.
    """

    model = AssetSource
    fields = ["name", "url", "license_type", "source_credit_text"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        obj = form.save()
        messages.success(self.request, _("Successfully created new asset source."))
        return HttpResponseRedirect(
            reverse_lazy("audio_asset_manager:source-detail", kwargs={"pk": obj.id})
        )


class AssetSourceDetailView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.DetailView
):
    """
    View the details of a given asset source.
    """

    model = AssetSource
    context_object_name = "source"


class AssetSourceUpdateView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.edit.UpdateView
):
    """
    Update the details of a given asset source.
    """

    model = AssetSource
    context_object_name = "source"

    def get_success_url(self):
        return reverse_lazy(
            "audio_asset_manager:source-detail", kwargs={"pk": self.get_object().id}
        )


class AssetSourceDeleteView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.edit.DeleteView
):
    """
    Delete a given asset source.
    """

    model = AssetSource
    context_object_name = "source"

    def get_success_url(self):
        messages.success(self.request, _("Deleted asset source!"))
        return reverse_lazy("audio_asset_manager:source-list")


# Artists


class ArtistListView(LoginRequiredMixin, generic.ListView):
    """
    View the artists in your asset library.
    """

    model = Artist
    prefetch_related = ["collection_set", "audioasset_set"]
    paginate_by = 25
    context_object_name = "artists"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise KeyError("A user needs to be logged in to access this page!")
        return self.model.objects.filter(owner=self.request.user)


class ArtistDetailView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.DetailView
):
    """
    View the details of the artist.
    """

    model = Artist
    prefetch_related = ["collection_set", "audioasset_set"]
    context_object_name = "artist"


class ArtistCreateView(LoginRequiredMixin, generic.edit.CreateView):
    """
    Create a new artist.
    """

    model = Artist

    def form_valid(self, form):
        form.instance.owner = self.request.user
        obj = form.save()
        messages.success(self.request, _("Created new artist!"))
        return HttpResponseRedirect(
            reverse_lazy("audio_asset_manager:artist-detail", kwargs={"pk": obj.id})
        )


class ArtistUpdateView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.edit.UpdateView
):
    """
    Update a given artist.
    """

    model = Artist
    fields = ["name"]
    context_object_name = "artist"

    def form_valid(self, form):
        obj = form.save()
        messages.success(self.request, _(f"Updated artist {obj.name}."))
        return HttpResponseRedirect(
            reverse_lazy("audio_asset_manager:artist-detail", kwargs={"pk": obj.id})
        )


class ArtistDeleteView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.edit.DeleteView
):
    """
    Delete a given artist.
    """

    model = Artist
    context_object_name = "artist"

    def get_success_url(self):
        return reverse_lazy("audio_asset_manager:artist-list")


# Collections
class CollectionDetailView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.DetailView
):
    """
    View the details of a collection.
    """

    model = Collection
    prefetch_related = ["audioasset_set"]
    context_object_name = "collection"


class CollectionCreateView(LoginRequiredMixin, generic.edit.CreateView):
    """
    Create a collection.
    """

    model = Collection
    form_class = CollectionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class CollectionUpdateView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.edit.UpdateView
):
    """
    Update a collection.
    """

    model = Collection
    context_object_name = "collection"
    form_class = CollectionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        obj = form.save()
        messages.success(self.request, _(f"Updated collection {obj.title}."))
        return HttpResponseRedirect(
            reverse_lazy("audio_asset_manager:collection-detail", kwargs={"pk": obj.id})
        )


class CollectionDeleteView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.edit.DeleteView
):
    """
    Delete a collection.
    """

    model = Collection
    context_object_name = "collection"

    def get_success_url(self):
        return reverse_lazy("audio_asset_manager:asset-list")


class AudioAssetListView(LoginRequiredMixin, generic.ListView):
    """
    View all your audio assets and filter by type.
    """

    model = AudioAsset
    select_related = ["artist", "collection", "source"]
    context_object_name = "assets"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise KeyError("A user needs to be logged in to access this page!")
        return self.model.objects.filter(owner=self.request.user)


class AudioAssetDetailView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.DetailView
):
    """
    View the details of an audio asset.
    """

    model = AudioAsset
    select_related = ["artist", "collection", "source"]
    context_object_name = "asset"


class AudioAssetCreateView(LoginRequiredMixin, generic.edit.CreateView):
    """
    Create a new audio asset.
    """

    model = AudioAsset
    form_class = AudioAssetForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        obj = form.save()
        messages.success(self.request, _(f"Created {obj.title}!"))
        return HttpResponseRedirect(
            reverse_lazy("audio_asset_manager:asset-detail", kwargs={"pk": obj.id})
        )


class AudioAssetUpdateView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.edit.UpdateView
):
    """
    Update an audio asset.
    """

    model = AudioAsset
    form_class = AudioAssetForm
    context_object_name = "asset"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(
            reverse_lazy("audio_asset_manager:asset-detail", kwargs={"pk": obj.id})
        )


class AudioAssetDeleteView(
    LoginRequiredMixin, AutoPermissionRequiredMixin, generic.edit.DeleteView
):
    """
    Delete an audio asset.
    """

    model = AudioAsset
    context_object_name = "asset"

    def get_success_url(self):
        messages.success(self.request, _("Deleted audio asset."))
        return reverse_lazy("audio_asset_manager:asset-list")
