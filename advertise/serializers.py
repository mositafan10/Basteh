from rest_framework import serializers
from .models import Packet, Travel, Offer, Bookmark, Report, Ticket
from account.serializers import CountrySerializer

class PacketSerializer(serializers.ModelSerializer):
    # problem with farsi ?!
    origin_country = serializers.StringRelatedField()
    origin_city = serializers.StringRelatedField()
    class Meta:
        model = Packet 
        fields = ['owner','origin_country','origin_city','destination_country','destination_city','category','weight','weight_unit','suggested_price','currency_price','place_of_get','place_of_give','start_date','end_date','buy','qr_code','visit_count','status','picture','slug']
class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel
        fields = ['owner','departure','departure_city','destination','destination_city','date_of_travel','empty_weight','unit_of_weight','ticket_picture','place_of_get_packet_traveler','place_of_give_packet_traveler','status'] 
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['packet','travel','price','currency'] 
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['owner','advertise'] 
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['owner','packet','text'] 
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['owner','date','airline','pic','is_approved'] 
