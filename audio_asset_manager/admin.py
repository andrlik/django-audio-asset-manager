# type: ignore
from django.contrib import admin

from .models import Artist, AssetSource, AudioAsset, Collection, LicenseType


class LicenseTypeAdmin(admin.ModelAdmin):
    ordering = ["name"]


class AssetSourceAdmin(admin.ModelAdmin):
    ordering = ["name", "owner"]
    list_display = ["name", "owner"]


class ArtistAdmin(admin.ModelAdmin):
    ordering = ["name"]


class CollectionAdmin(admin.ModelAdmin):
    ordering = ["album_artist__name", "title", "owner"]
    list_display = ["title", "album_artist", "owner"]


class AudioAssetAdmin(admin.ModelAdmin):
    ordering = ["owner", "artist", "collection", "title"]
    list_display = ["owner", "artist", "title", "source", "collection"]


admin.site.register(LicenseType, LicenseTypeAdmin)
admin.site.register(AssetSource, AssetSourceAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(AudioAsset, AudioAssetAdmin)
