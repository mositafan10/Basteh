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
from rest_framework.authtoken.models import Token
from .utils import generate_otp,set_otp, verify_otp, send_sms
from .models import Profile, Social, Score, CommentUser, City, Country, Follow, User
from .serializers import *
from .permissions import IsOwnerProfileOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken


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
    send_sms(phone_number, otp)
    return HttpResponse(status=200)


# @api_view(['POST'])
# @permission_classes((AllowAny,))
# def create_user(request):
#     serialized = UserSerializer(data=request.data)
#     if serialized.is_valid():
#         User.objects.create_user(
#             serialized.save()
#         )
#         return Response(serialized.data, status=201)
#     else:
#         return Response(serialized._errors, status=400)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verification(request):
    phone_number = request.GET['phone_number']
    refresh = None
    user, is_created = User.objects.get_or_create(phone_number=phone_number)
    if is_created==False and 'password' in request.GET:
        user.check_password(request.GET['password'])
        refresh = RefreshToken.for_user(user)
    otp = request.GET.get('otp', None)
    if verify_otp(phone_number, otp):
        if is_created is True:
            user.save()
        refresh = RefreshToken.for_user(user)
    if refresh is not None:
        return JsonResponse({"token": str(refresh.access_token),
                             "refresh": str(refresh)})
    else:
        raise ValidationError()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_user(request):
    print(request.user)
    return JsonResponse({})


# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def update_profile(request):



# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def login(request):
#     username = request.GET['username']
#     password = request.GET['password']
#     if username is None or password is None:
#         return Response({'error': 'Please provide both username and password'},
#                         status=HTTP_400_BAD_REQUEST)
#     user = authenticate(username=username, password=password)
#     if not user:
#         return Response({'error': 'Invalid Credentials'},
#                         status=HTTP_404_NOT_FOUND)
#     token, _ = Token.objects.get_or_create(user=user)
#     return Response({'token': token.key},
#                     status=HTTP_200_OK)


# @api_view(['GET', 'POST'])
# @permission_classes([permissions.AllowAny])
# def profile_list(request):
#     if request.method == 'GET':
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(profiles, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ProfileSerializer(data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


# @api_view(['GET','PUT','DELETE'])
# @permission_classes([permissions.AllowAny])
# def profile_detail(request, pk):
#     try:
#         profiles = Profile.objects.get(pk=pk)
#     except Profile.DoesNotExist:
#         return HttpResponse(status=404)
#     if request.method == 'GET':
#         serializer = ProfileSerializer(profiles)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'PUT':
#         if request.user.is_authenticated:
#             data = JSONParser.parse(request)
#             serializer = ProfileSerializer(data=data)
#         else:
#             raise PermissionDenied
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         if not request.user.is_authenticated:
#             raise PermissionDenied
#         profiles.delete()
#         return HttpResponse(status=204)


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
