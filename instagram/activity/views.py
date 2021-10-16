from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from activity.models import Comment
from activity.serializers import CommentSerializer

"""
                            #####       API         ####
"""


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
