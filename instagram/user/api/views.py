from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.api.serializers import UserSerializer, UserLightSerializer

User = get_user_model()

#base type
# class ProfileRetrieveAPIView(APIView):
# def get(self, request, username, *args, **kwargs):
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         return Response({'error: this isn\'t exists'})
#     serializer = UserSerializer(instance=user)
#     return Response(serializer.data)


#Generic type
class ProfileRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ProfileListAPIView(ListAPIView):
    serializer_class = UserLightSerializer
    queryset = User.objects.all()
