from django.contrib import admin

from .models import User, listings, biddings, winners, comments
# Register your models here.
admin.site.register(User)
admin.site.register(listings)
admin.site.register(biddings)
admin.site.register(winners)
admin.site.register(comments)