import rules
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Put your models here.
from model_utils.models import TimeStampedModel
from rules.contrib.models import RulesModelBase, RulesModelMixin
from taggit.managers import TaggableManager

from .rules import is_object_owner


class AbstractOwnedModel(RulesModelMixin, models.Model, metaclass=RulesModelBase):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=_("User who owns this record."),
    )

    class Meta:
        abstract = True
        rules_permissions = {
            "add": rules.is_authenticated,
            "read": is_object_owner,
            "change": is_object_owner,
            "delete": is_object_owner,
            "view": is_object_owner,
        }


class LicenseType(TimeStampedModel):
    """
    Model representing typical license type for assets.
    """

    name = models.CharField(max_length=250, help_text=_("Name for the license."))
    url = models.URLField(
        null=True, blank=True, help_text=_("URL for the license type, if applicable.")
    )
    include_license_in_credits = models.BooleanField(
        default=False,
        help_text=_("Do we need to include this license term in the credits?"),
    )

    def __str__(self):  # pragma: nocover
        return self.name

    class Meta:
        ordering = ["name"]


class AssetSource(AbstractOwnedModel, TimeStampedModel):
    name = models.CharField(
        max_length=100,
        help_text=_(
            "Name for this source of assets. May be an artist if licensed directly or a service, e.g. Audiio."
        ),
    )
    url = models.URLField(
        null=True, blank=True, help_text=_("URL for the source, if applicable.")
    )
    license_type = models.ForeignKey(
        "LicenseType",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Licensing this source uses."),
    )
    source_credit_text = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=_(
            "Additional credit information if required, e.g. / via Adobe Stock"
        ),
    )

    def __str__(self):  # pragma: nocover
        return self.name


class Artist(AbstractOwnedModel, TimeStampedModel):
    """
    An artist that created assets, e.g. a musician, producer, or company.
    """

    name = models.CharField(max_length=250, help_text=_("Name for artist"))

    def __str__(self):  # pragma: nocover
        return self.name


class Collection(AbstractOwnedModel, TimeStampedModel):
    """
    A collection or album of assets.
    """

    title = models.CharField(
        max_length=250, help_text=_("Title of album or collection.")
    )
    album_artist = models.ForeignKey(
        "Artist", null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):  # pragma: nocover
        return self.title


class AudioAsset(AbstractOwnedModel, TimeStampedModel):
    """
    An audio asset model.
    """

    class AssetTypes(models.TextChoices):
        MUSIC = "MU", _("Music")
        SFX = "SFX", _("SFX")
        AD = "AD", _("Ad")
        PROMO = "PR", _("Promo")

    asset_type = models.CharField(
        max_length=5,
        choices=AssetTypes.choices,
        default=AssetTypes.MUSIC,
        help_text=_("Type of asset."),
        db_index=True,
    )
    title = models.CharField(
        max_length=250, help_text=_("The title or name of the asset.")
    )
    artist = models.ForeignKey(
        "Artist",
        help_text=_("The artist to when crediting this asset."),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    collection = models.ForeignKey(
        "Collection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Collection or album this asset is from, if applicable."),
    )
    filename = models.CharField(
        max_length=250,
        help_text=_("Original filename when added, if done via a scan."),
        null=True,
        blank=True,
    )
    digest = models.CharField(
        max_length=50,
        help_text=_("Original SHA1 digest of file, if originally added via a scan."),
        null=True,
        blank=True,
    )
    source = models.ForeignKey(
        "AssetSource",
        null=True,
        blank=True,
        help_text=_("Source that licensed this asset to us, if applicable."),
        on_delete=models.SET_NULL,
    )
    explicit_credit_required = models.BooleanField(
        default=True,
        help_text=_(
            "Is explicit per asset credit required or can attribution be grouped?"
        ),
    )
    credit_link = models.URLField(
        null=True,
        blank=True,
        help_text=_("URL to use when providing credit, if required."),
    )
    duration = models.PositiveIntegerField(
        default=0, help_text=_("Length of audio file in seconds.")
    )
    bpm = models.PositiveIntegerField(
        null=True, blank=True, help_text=_("BPM of the file, if applicable.")
    )
    loudness = models.FloatField(
        null=True, blank=True, help_text=_("Integrated LUFS of the file, if measured.")
    )
    tags = TaggableManager()

    def __str__(self):  # pragma: nocover
        return f"{self.title} - {self.artist}"
