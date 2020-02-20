from django.shortcuts import HttpResponse
from django.http import JsonResponse 
from .models import Packet, Travel, Offer, Bookmark, Report, Ticket
from .serializers import PacketSerializer, TravelSerializer, OfferSerializer, BookmarkSerializer, ReportSerializer, TicketSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status


@csrf_exempt
def packet_list(request):
    if request.method == 'GET':
        packet = Packet.objects.all()
        serializer = PacketSerializer(packet, many=True,)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser.parse(request)
        serializer = PacketSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(seializer.errors, status=400)

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def travel_detail(request, pk):
    try:
        travel = Travel.objects.get(pk=pk)
    except Travel.DoesNotExist :
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
    elif request.method == "DELETE":
        travel.delete()
        return HttpResponse(status=204)

