from django.contrib import admin
from .models import Author, Trade, TradeImage
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Author)
admin.site.register(Trade)
admin.site.register(TradeImage)