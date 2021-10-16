from rest_framework import serializers

from relation.models import Relation
from user.api.serializers import UserSerializer, UserLightSerializer

"""
can be completed now just show the people who has done follow back
"""


class RelationSerializer(serializers.ModelSerializer):
    from_user = UserLightSerializer()
    followed_back = serializers.SerializerMethodField()

    class Meta:
        model = Relation
        fields = ('from_user', 'followed_back', 'created_time')

    def get_followed_back(self, obj):
        return Relation.objects.filter(following=obj.following, follower=obj.follower).exists()
