from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .models import Profile, Social, Score, CommentUser, City, Country, Follow
from .serializers import ProfileSerializer, SocialSerializer, ScoreSerializer, ScoreSerializer, CommentUserSerializer, CitySerializer, CountrySerializer, FollowSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from .utils import generate_otp, set_otp


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_otp(request, phone):
    otp = generate_otp()
    set_otp(phone, otp)
    return json({"otp": otp})

       
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_otp(request):
    token, is_created = Token.object.get_or_create(user=request.user)


@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def profile_list(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.AllowAny])
def profile_detail(request, pk):
    try:
        profiles = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':

        serializer = ProfileSerializer(profiles)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            data = JSONParser.parse(request)
            serializer = ProfileSerializer(data=data)
        else:
            raise PermissionDenied
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            raise PermissionDenied
        profiles.delete()
        return HttpResponse(status=204)


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
