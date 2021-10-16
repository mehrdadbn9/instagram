from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from activity.models import Comment
from relation.models import Relation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment', 'post', 'reply')

    def validate(self, attrs):
        request = self.context['request']

        if attrs['reply'] is not None and attrs['reply'].post != attrs['post']:
            raise ValidationError(_("Post and comment post are not the same"))

        if request.user != attrs['post'].user and not Relation.objects.filter(
                from_user=request.user, to_user=attrs['post'].user).exists():
            raise ValidationError(_("You are not allowed to do this action"))

        return attrs
