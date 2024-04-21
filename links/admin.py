from django.contrib import admin

from .models import Collection, Link


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "created_at",
        "updated_at",
        "user",
    )


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "url",
        "image",
        "link_type",
        "created_at",
        "updated_at",
    )
