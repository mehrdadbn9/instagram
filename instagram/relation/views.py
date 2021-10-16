from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from content.models import Stream, Post
from relation.models import Relation

# from relation.serializers import RelationSerializer
from relation.serializers import RelationSerializer
from user.api.serializers import UserSerializer

User = get_user_model()


###class base
class FollowView(View):
    pattern_name = 'profile'

    def get_object(self):
        try:

            user = User.objects.get(username=self.kwargs.get('username'))  # can change to object_or_404
        except User.DoesNotExists:
            raise Http404
        return user

    def post(self, request, *args, **kwargs):

        target_user = self.get_object()
        if target_user == request.user:
            return redirect(f'/{target_user.username}/')
        qs = Relation.objects.filter(following=request.user, follower=target_user)
        if qs.exists():
            qs.delete()
            Stream.objects.filter(user=request.user, following=target_user).all().delete()
        else:
            with transaction.atomic():
                Relation.objects.create(following=request.user, follower=target_user)
                target_user.followers_count += 1
                target_user.save()
                request.user.followings_count += 1
                request.user.save()

                # for post in Post:
                #     stream = Stream(post=post, user=request.user, following=target_user)
                #     stream.save()
        return redirect(f'/{target_user.username}/')


class FollowBackListAPIView(ListAPIView):
    queryset = Relation.objects.select_related('following').all()
    serializer_class = RelationSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(follower=self.request.user)
