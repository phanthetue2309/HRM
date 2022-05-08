import uuid

from api_base.models import TimeStampedModel
from api_office.models import Office
from api_user.managers import ProfileManager
from api_user.models import User
from common.constants.user_constants import Genders
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone


def name_file(instance, filename):
    return "/".join([str(instance.id), filename])


class Profile(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=255, null=True)
    personal_email = models.EmailField(max_length=255, null=True)
    birth_day = models.DateField(null=True)
    slack_id = models.CharField(max_length=255, null=True)
    phone = models.CharField(
        max_length=11,
        null=True,
        validators=[
            RegexValidator(regex=r"^\d+$", message="A valid integer is required."),
            MinLengthValidator(9),
        ],
    )
    gender = models.CharField(
        choices=Genders.GENDERS, default=Genders.Select, max_length=100
    )
    teams = models.CharField(max_length=100, default="")
    office = models.ForeignKey(Office, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(
        upload_to=name_file, max_length=255, blank=True, null=True
    )
    join_date = models.DateField(default=timezone.now)
    veggie = models.BooleanField(default=False)
    auto_booking_lunch = models.BooleanField(default=False)
    line_manager = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    maximum_level_approved = models.IntegerField(default=1, blank=True)

    objects = ProfileManager()

    class Meta:
        db_table = "hr_profiles"

    @property
    def photo_value(self):
        # noinspection PyUnresolvedReferences
        return self.photo

    @property
    def image_attr(self):
        return self.image
