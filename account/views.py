from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions, generics
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from .utils import generate_otp,set_otp, verify_otp, send_sms
from .models import Profile, Social, Score, CommentUser, City, Country, Follow, User
from .serializers import *
from .permissions import IsOwnerProfileOrReadOnly


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerProfileOrReadOnly]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    phone_number = request.GET['phone_number']
    otp = generate_otp()
    print (otp)
    set_otp(phone_number, otp)
    # send_sms(phone_number, otp)
    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    phone_number = request.GET['phone_number']
    password = request.GET.get('password', None)
    refresh = None
    user, is_created = User.objects.get_or_create(phone_number=phone_number)
    if is_created==False and password is not None:
        if user.check_password(request.GET['password']):
            refresh = RefreshToken.for_user(user)
        else:
            error = "Your password is incorrect"
    otp = request.GET.get('otp', None)
    if otp is not None:
        if verify_otp(phone_number, otp):
            if is_created is True:
                user.save()
            refresh = RefreshToken.for_user(user)
        else :
            error = "The code is incorrect"
    if refresh is not None:
        return JsonResponse({"token": str(refresh.access_token),
                             "refresh": str(refresh)})
    else:
        raise ValidationError(error)

@permission_classes([permissions.AllowAny])
@api_view(['POST'])
def reset_password(request):
    # phone_number = request.GET['phone_number']
    # user = User.objects.get(phone_number=phone_number)
    # if request.user == user:
    #     otp = generate_otp()
    #     user.set_password (otp)
    #     # send_sms(phone_number, otp)
    #     return HttpResponse(status=200)
    pass

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_user(request):
    user = User.objects.get(phone_number=request.user)
    password = request.GET.get('password', None)
    first_name = request.GET.get('first_name', None)
    last_name = request.GET.get('last_name', None)
    user.set_password(password) 
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    profile, is_created = Profile.objects.get_or_create(user=request.user)
    bio = request.GET.get('bio', None) # does not work TODO
    country = request.GET.get('country', None)
    city = request.GET.get('city', None)
    birthday = request.GET.get('birthday', None)
    favorite_gift = request.GET.get('favorite_gift', None)
    profile.bio = bio
    profile.country = country
    profile.city = city
    profile.birthday = birthday
    profile.favorite_gift = favorite_gift
    profile.save()
    return JsonResponse({"Result" : True})


@api_view(['GET', 'PUT', 'DELETE'])
def social_detail(request, pk):
    try:
        social = Social.object.get(pk=pk)
    except Social.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = SocialSerializer(social)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serialzer = SocialSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        social.delete()
        return HttpResponse(status=204)
