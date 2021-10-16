from rest_framework import serializers

from content.models import Post, Media
# from location.serializers import LocationSerializer
from user.api.serializers import UserLightSerializer


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('media_file',)


class PostListSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    # location = LocationSerializer()
    media = PostMediaSerializer(many=True)

    class Meta:
        model = Post
        # TODO: Add post_tag and tagged_user to the list API
        # TODO: Likes and Comments count
        fields = ('id', 'caption', 'user', 'media')


########################## should complete
class PostHyperlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["user", "url"]


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


#################################################
class PostCreateSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    media = PostMediaSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'caption', 'user', 'media')
