from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Packet, Travel, Offer, Bookmark, Report, Ticket
from .serializers import *
from .permissions import IsOwnerPacketOrReadOnly


@permission_classes([permissions.AllowAny])
@api_view(['GET', 'POST'])
def packet_list(request):
    if request.method == 'GET':
        packet = Packet.objects.all()
        serializer = PacketSerializer(packet, many=True,)
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser.parse(request)
        serializer = PacketSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(seializer.errors, status=400)


@permission_classes([AllowAny])
@api_view(['GET'])
def user_packet_list(request):
    if request.method == 'GET':
        packet = Packet.objects.all()
        serializer = PacketSerializer(packet, many=True)
        return JsonResponse(serializer.data)

@permission_classes([permissions.AllowAny])
@api_view(['PUT'])
def update_packet(request, pk):
    if request.method == 'PUT':
        packet = Packet.objects.get(pk=pk)
        if request.user == packet.owner.user :
            data = JSONParser.parse(request)
            serializer = PacketSerializer(data=data)
            if serialzier.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.error, status=400)
        return JsonResponse({"Access Deneid" : "You have not permision to edit this packet"}, status=400)

@permission_classes([permissions.AllowAny])
@api_view(['GET', 'PUT', 'DELETE'])
def packet_detail(request, pk):
    try:
        packet = Packet.objects.get(pk=pk)
    except Packet.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serilaizer = PacketSerializer(packet)
        return JsonResponse(serilaizer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = PacketSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serialzier.errors, status=400)
    elif request.method == 'DELETE':
        packet.delete()
        return HttpResponse(status=204)


@permission_classes([permissions.AllowAny])
@api_view(['GET', 'POST'])
def travel_list(request):
    travel = Travel.objects.all()
    serializer = TravelSerializer(travel, may=True)
    if request.method == 'GET':
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser.parse(request)
        serializer = TravelSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)


@permission_classes([permissions.AllowAny])
@api_view(['GET', 'PUT', 'DELETE'])
def travel_detail(request, pk):
    try:
        travel = Travel.objects.get(pk=pk)
    except Travel.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = TravelSerializer(travel)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = TravelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        travel.delete()
        return HttpResponse(status=204)

@permission_classes([AllowAny])
@api_view(['GET','POST'])
def visit_packet(request, pk):
    try:
        packet = Packet.objects.get(pk=pk)
    except Packet.DoesNotExist:
        return HttpResponse(status=404)
    packet = Packet.objects.get(pk=pk)
    model_name = "visit_packet"
    ip = request.META.get("HTTP_REMOTE_ADDR")
    key = "%s_%s" % (model_name, ip)
    if not cache.get(key) == pk:
        cache.set(key, pk, 4)
        packet.visit()
        return HttpResponse(status=201)
    return HttpResponse(status=400)

@permission_classes([AllowAny])
@api_view(['GET','POST'])
def visit_travel(request, pk):
    try:
        travel = Travel.objects.get(pk=pk)
    except Travel.DoesNotExist:
        return HttpResponse(status=404)
    travel = Travel.objects.get(pk=pk)
    model_name = "visit_travel"
    ip = request.META.get("HTTP_REMOTE_ADDR")
    key = "%s_%s" % (model_name, ip)
    if not cache.get(key) == pk:
        cache.set(key, pk, 4)
        travel.visit()
        return HttpResponse(status=201)
    return HttpResponse(status=400)