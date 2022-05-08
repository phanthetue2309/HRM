from api_workday.models.leave_type import LeaveType
from rest_framework import serializers


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["name_type"] = instance.leave_type_group.name
        return ret

    def create(self, validated_data):
        if not LeaveType.objects.filter(name=validated_data["name"]).exists():
            return LeaveType.objects.create(**validated_data)
        return None
