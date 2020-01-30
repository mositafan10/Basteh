from django.contrib import admin
from .models import PacketAds, TravelAds, Offer, AdsBookmark


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('owner_user_name', 'origin_country_packet',
                    'destination_country_packet', 'categoty_of_packet', 'buy_by_traveler', 'create_at', 'status')

    list_editable = ('status',)
    list_filter = ('origin_country_packet',
                   'categoty_of_packet', 'owner_of_packet__username')
    raw_id_fields = ("owner_of_packet",)  # no understand
    search_fields = ('owner_of_packet__username', 'categoty_of_packet')

    def owner_user_name(self, obj):
        return obj.owner_of_packet.username


admin.site.register(PacketAds, AuthorAdmin)
admin.site.register(TravelAds)
admin.site.register(Offer)
admin.site.register(AdsBookmark)
