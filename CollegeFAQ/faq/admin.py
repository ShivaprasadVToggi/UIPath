from django.contrib import admin
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'question', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('question', 'answer')
    list_per_page = 25
    fields = ('category', 'question', 'answer')
