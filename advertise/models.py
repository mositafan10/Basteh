from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseAds (models.Model):
    id = models.AutoField(primary_key=True)
    create_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class PacketAds (BaseAds):

    STATUS_CHOICES = [
    ('wfa', 'wait_for_approving'),
    ('p', 'Published'),
    ('wo', 'With_offer'),
    ('abu','accept_by_users'),
    ('s','sended'),
    ]

    PACKET_CATEGORY = [
        ('doc','Document'),
        ('bok','Book'),
    ]
    
    owner_of_packet = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'owner_of_packet')
    origin_country_packet = models.CharField(
        "origin_country_packet", max_length=50)  # need choices
    destination_country_packet = models.CharField(
        "destination_country_packet", max_length=50)  # need choices
    origin_city = models.CharField(
        "origin_city", max_length=50)  # need choices
    destination_city = models.CharField(
        "destination_city", max_length=50)  # need choices
    categoty_of_packet = models.CharField(
        "categoty_of_packet", max_length=20, choices = PACKET_CATEGORY)  # need choices
    weight_of_packet = models.PositiveIntegerField("weight_of_packet")
    dimension_of_packet = models.PositiveIntegerField(
        "dimension_of_packet")  # need 3 field for dimension
    suggested_price = models.PositiveIntegerField(
        "suggested_price")  # need currency sign
    place_of_get_packet = models.CharField(
        "place_of_get_packet", max_length=20)  # need choices
    place_of_give_packet = models.CharField(
        "place_of_give_packet", max_length=20)  # need choices
    date_of_send_packet = models.DurationField(
        "date_of_send_packet")  # need date interval and should be future //*TODO*//
    buy_by_traveler = models.BooleanField("buy_by_traveler")
    qr_code = models.CharField("qr_code", max_length=100)
    ads_visit_count = models.IntegerField("ads_visit_count")
    status = models.CharField(max_length = 3, choices =STATUS_CHOICES, )

    def __str__ (self):
        return "HI"
    

class TravelAds (BaseAds):
    departure_country_traveler = models.CharField(
        "departure_country_traveler", max_length=50)
    destination_country_traveler = models.CharField(
        "destination_country_traveler", max_length=50)
    date_of_travel = models.DateTimeField("date_of_travel") # should be future
    empty_weight = models.IntegerField("empty_weight")
    ticket_picture = models.FileField("ticket_picture")
    place_of_get_packet_traveler = models.CharField("place_of_get_packet_traveler",
                                                    max_length=20)  # need choices
    place_of_give_packet_traveler = models.CharField("place_of_give_packet_traveler",
                                                     max_length=20)  # need choices


class Offer (BaseAds):
    packet_ads = models.ForeignKey(
        PacketAds, on_delete=models.CASCADE, related_name="packet_ads")
    travel_ads = models.ForeignKey(
        TravelAds, on_delete=models.CASCADE, related_name="travel_ads")
    offer_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="offer_by")
    offer_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="offer_to")
    offer_price = models.IntegerField("offer_price")  # need currency


class AdsBookmark (BaseAds):
    booked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="booked_by")
    booked_ads = models.ForeignKey(
        PacketAds, on_delete=models.CASCADE, related_name="booked_ads")
