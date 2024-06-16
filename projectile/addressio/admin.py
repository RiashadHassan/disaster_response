from django.contrib import admin

from .models import Address, District, Division, Upazila, PostOffice, AddressConnector

admin.site.register(Address),
admin.site.register(AddressConnector),
admin.site.register(Division),
admin.site.register(Upazila),
admin.site.register(District),
admin.site.register(PostOffice),
