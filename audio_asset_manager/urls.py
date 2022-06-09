from django.urls import path

from .views import (
    ArtistCreateView,
    ArtistDeleteView,
    ArtistDetailView,
    ArtistListView,
    ArtistUpdateView,
    AssetSourceCreateView,
    AssetSourceDeleteView,
    AssetSourceDetailView,
    AssetSourceListView,
    AssetSourceUpdateView,
    AudioAssetCreateView,
    AudioAssetDeleteView,
    AudioAssetDetailView,
    AudioAssetListView,
    AudioAssetUpdateView,
    CollectionCreateView,
    CollectionDeleteView,
    CollectionDetailView,
    CollectionUpdateView,
)

app_name = "audio_asset_manager"

urlpatterns = [  # type: ignore
    # Add your url paths here.
    path("sources/", view=AssetSourceListView.as_view(), name="source-list"),
    path("sources/create/", view=AssetSourceCreateView.as_view(), name="source-create"),
    path(
        "sources/<int:pk>/", view=AssetSourceDetailView.as_view(), name="source-detail"
    ),
    path(
        "sources/<int:pk>/edit/",
        view=AssetSourceUpdateView.as_view(),
        name="source-update",
    ),
    path(
        "sources/<int:pk>/delete/",
        view=AssetSourceDeleteView.as_view(),
        name="source-delete",
    ),
    path("artists/", view=ArtistListView.as_view(), name="artist-list"),
    path("artists/create/", view=ArtistCreateView.as_view(), name="artist-create"),
    path("artists/<int:pk>/", view=ArtistDetailView.as_view(), name="artist-detail"),
    path(
        "artists/<int:pk>/edit/", view=ArtistUpdateView.as_view(), name="artist-update"
    ),
    path(
        "artists/<int:pk>/delete/",
        view=ArtistDeleteView.as_view(),
        name="artist-delete",
    ),
    path(
        "collections/create/",
        view=CollectionCreateView.as_view(),
        name="collection-create",
    ),
    path(
        "collections/<int:pk>/",
        view=CollectionDetailView.as_view(),
        name="collection-detail",
    ),
    path(
        "collections/<int:pk>/edit/",
        view=CollectionUpdateView.as_view(),
        name="collection-update",
    ),
    path(
        "collections/<int:pk>/delete/",
        view=CollectionDeleteView.as_view(),
        name="collection-delete",
    ),
    path("assets/", view=AudioAssetListView.as_view(), name="asset-list"),
    path("assets/create/", view=AudioAssetCreateView.as_view(), name="asset-create"),
    path("assets/<int:pk>/", view=AudioAssetDetailView.as_view(), name="asset-detail"),
    path(
        "assets/<int:pk>/edit/",
        view=AudioAssetUpdateView.as_view(),
        name="asset-update",
    ),
    path(
        "assets/<int:pk>/delete/",
        view=AudioAssetDeleteView.as_view(),
        name="asset-delete",
    ),
]
