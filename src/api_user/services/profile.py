from api_base.services import BaseService
from api_user.models import Profile
from api_user.serializers import ProfileSerializers


class ProfileService(BaseService):
    @classmethod
    def update_list_auto_booking(cls, profiles, status):
        list_pk = [profile["id"] for profile in profiles]
        update_profiles = Profile.objects.filter(id__in=list_pk).update(
            auto_booking_lunch=status
        )
        return update_profiles

    @classmethod
    def update_slack_id_by_profile_id(cls, profile_id, slack_id):
        return Profile.objects.filter(pk=profile_id).update(slack_id=slack_id)

    @classmethod
    def get_profile_by_slack_id(cls, slack_id: str):
        return Profile.objects.filter(slack_id=slack_id).first()

    @classmethod
    def get_profile_by_email(cls, personal_email):
        return Profile.objects.filter(personal_email=personal_email).first()

    @classmethod
    def get_profile_by_user_id(cls, user_id):
        return Profile.objects.filter(user_id=user_id).first()

    @classmethod
    def get_all_profile(cls):
        profiles = Profile.objects.all()
        profile_serializers = ProfileSerializers(profiles, many=True)
        return profile_serializers.data
