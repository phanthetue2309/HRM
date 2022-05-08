from api_base.services import BaseService
from api_team.models import Team, TeamMembers
from api_user.models import Profile, Role, Titles, User
from api_user.serializers.profile import TeamProfile
from api_user.services import UserService
from common.constants.user_constants import TitleConstant
from django.db.models import Q


class TeamService(BaseService):
    # get all members of a team
    @classmethod
    def get_members_in_team(cls, team_id):
        return list(
            TeamMembers.objects.filter(team_id=team_id).values_list(
                "member_id", flat=True
            )
        )

    @classmethod
    def update_line_manager_in_team(cls, team):
        leader = team.team_leader
        if leader:
            team_members = TeamMembers.objects.filter(team_id=team.id)
            for team_member in team_members:
                member = team_member.member
                if member.profile.line_manager != leader.profile:
                    member.profile.line_manager = leader.profile
                    member.profile.teams = team.team_name
                    member.profile.office = team.office
                    member.profile.save()

    # check this user has a team or not
    @classmethod
    def check_had_team(cls, user_id):
        return bool(TeamMembers.objects.filter(member_id=user_id).first())

    @classmethod
    def check_in_team(cls, user, team_id):
        return bool(TeamMembers.objects.filter(team_id=team_id, member=user).first())

    # check whether pm has team or not
    @classmethod
    def check_owner_team(cls, user, team_id):
        if user.staff:
            return True
        return Team.objects.filter(id=team_id, team_leader_id=user.id)

    # get team of current user
    @classmethod
    def get_team(cls, user_id):
        return list(
            TeamMembers.objects.filter(member_id=user_id).values_list(
                "team_id", flat=True
            )
        )

    @classmethod
    def add_new_member(cls, instance, **kwargs):
        user = UserService.get_user_by_email(kwargs.get("email"))
        if user:
            cls.update_user_team(user, instance.id)

    @classmethod
    def remove_member(cls, data, instance):
        user = UserService.get_user_by_email(data.get("email"))
        if user:
            cls._remove_user_team(user, instance.id)
            user.profile.save()

    @classmethod
    def delete_team(cls, team):
        Profile.objects.filter(teams=team.team_name).update(teams="", line_manager=None)
        team.team_leader.title.remove(
            Titles.objects.get(title=TitleConstant.TITLES[6][0])
        )
        TeamMembers.objects.filter(team_id=team.id).delete()

    @classmethod
    def get_leader(cls, text=None, limit=10):
        if text is None:
            text = ""
        users = (
            User.objects.select_related("profile")
            .filter(profile__name__istartswith=text, staff=0)
            .exclude(title__title=TitleConstant.TITLES[2][0])
            .select_related("leader")
            .filter(leader__team_leader__isnull=True)[:limit]
        )
        return [
            {"id": user.id, "email": user.email, "name": user.profile.name}
            for user in users
        ]

    @classmethod
    def get_potential_members(cls):
        profiles = (
            Profile.objects.select_related("user")
            .filter(user__active=1)
            .exclude(Q(user__staff=True))
        )
        return [
            {"id": profile.user.id, "name": profile.name, "email": profile.user.email}
            for profile in profiles
            if not cls.check_had_team(profile.user.id)
        ]

    @classmethod
    def modify_members(cls, team, member_ids):
        existed_members = TeamMembers.objects.filter(team=team.id)
        team_leader = Team.objects.filter(id=team.id).first().team_leader
        if not member_ids:
            existed_members.delete()

        existed_members = existed_members.all()
        member_ids = {str_id.replace("-", "") for str_id in member_ids.split(",")}
        deleted_ids = set()
        stable_ids = set()

        for existed_member in existed_members:
            str_id = str(existed_member.member.id).replace("-", "")
            if str_id not in member_ids:
                deleted_ids.add(str_id)
            else:
                stable_ids.add(str_id)
        existed_members.filter(member__in=deleted_ids).exclude(
            member=team_leader.id.hex
        ).delete()
        for deleted_id in deleted_ids:
            deleted_user = User.objects.get(id=deleted_id)
            Profile.objects.filter(user=deleted_user).update(teams="")

        added_ids = member_ids - (deleted_ids.union(stable_ids))
        added_objects = []
        for added_id in added_ids:
            added_objects.append(TeamMembers(team_id=team.id, member_id=added_id))
            added_user = User.objects.filter(id=added_id).first()
            if added_user and team.team_leader and team.team_leader != added_user:
                added_user.profile.line_manager = team.team_leader.profile
                added_user.profile.teams = team.team_name
                added_user.profile.office = team.office
                added_user.profile.save()
        TeamMembers.objects.bulk_create(added_objects)

    @classmethod
    def get_profile(cls, data, instance, leaders):
        check = True
        data.update(leader_name="No leader")
        if data.get("team_leader"):
            for leader in leaders:
                if cls.leader_accept(data, leader):
                    data.update(leader_name=leader.get("name", "No leader"))
                    check = False
                    break
        if check:
            data.update(team_leader=0)
        team_member_ids = cls.get_members_in_team(instance.pk)
        profiles = Profile.objects.filter(user_id__in=team_member_ids)
        for profile in profiles:
            profile.team_leader_id = data.get("team_leader")
        data.update(
            employee_number=profiles.count(),
            employee_list=TeamProfile(profiles, many=True).data,
        )
        return data

    @classmethod
    def leader_accept(cls, data, leader):
        return (
            data.get("team_leader") == leader.get("user_id")
            and leader.get("user__active")
            # and cls.check_in_team(leader.get("user_id"), data.get("id"))
        )

    @classmethod
    def update_user_team(cls, user, team_id):
        team = Team.objects.get(pk=team_id)
        if not cls.check_had_team(user.id):
            if not cls.check_in_team(user, team_id):
                TeamMembers.objects.create(member=user, team=team)
        else:
            TeamMembers.objects.filter(member=user).update(team=team)
        if team.team_leader and team.team_leader != user:
            user.profile.line_manager = team.team_leader.profile
            user.profile.teams = team.team_name
            user.profile.office = team.office
            user.profile.save()

    @classmethod
    def _remove_user_team(cls, member, team_id):
        TeamMembers.objects.filter(member_id=member.id, team_id=team_id).delete()
        users = User.objects.get(pk=member.id)
        Profile.objects.filter(user=users).update(teams="")

    @classmethod
    def set_leader(cls, team, **kwargs):
        email = kwargs.get("email")
        user = UserService.get_user_by_email(email)
        if user:
            team.team_leader = user
            team.save()
            user.title.add(Titles.objects.get(title=TitleConstant.TITLES[6][0]))
            user.save()
            cls.update_line_manager_in_team(team)
            cls.update_user_team(user, team.id)

    @classmethod
    def move_team(cls, user_id, current_team_id, new_team_id):
        user = User.objects.get(id=user_id)
        cls._remove_user_team(user, current_team_id)
        cls.update_user_team(user, new_team_id)

    @classmethod
    def update_role_leader(cls, instance, validated_data):
        leader_current = instance.team_leader
        leader_new = validated_data.get("team_leader")
        leader_role, created = Role.objects.get_or_create(
            name="Team Leader",
            description="Access for team leader.",
        )
        leader_current.roles.remove(leader_role)
        leader_new.roles.add(leader_role)
        leader_current.title.remove(
            Titles.objects.get(title=TitleConstant.TITLES[6][0])
        )
        leader_new.title.add(Titles.objects.get(title=TitleConstant.TITLES[6][0]))
