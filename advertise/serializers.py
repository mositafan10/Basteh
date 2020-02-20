from rest_framework import serializers
from .models import Packet, Travel, Offer, Bookmark, Report, Ticket
from account.serializers import CountrySerializer, CitySerializer


class PacketSerializer(serializers.ModelSerializer):
    origin_country = CountrySerializer()
    destination_country = CountrySerializer()
    origin_city = CitySerializer()
    destination_city = CitySerializer()

    class Meta:
        model = Packet
        fields = "__all__"


class TravelSerializer(serializers.ModelSerializer):
    origin_country = CountrySerializer()
    destination_country = CountrySerializer()
    origin_city = CitySerializer()
    destination_city = CitySerializer()

    class Meta:
        model = Travel
        fields = "__all__"

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['packet', 'travel', 'price', 'currency']


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['owner', 'advertise']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['owner', 'packet', 'text']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['owner', 'date', 'airline', 'pic', 'is_approved']
