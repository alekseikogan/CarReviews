from django.contrib import admin

from .models import Car, Body, Mark


class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'mark', 'model', 'complect', 'body', 'year', 'photo', 'time_create')
    list_display_links = ('id', 'model')
    search_fields = ('mark', 'model', 'body')
    prepopulated_fields = {'slug': ('model',)}


class BodyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class MarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Car, CarAdmin)
admin.site.register(Body, BodyAdmin)
admin.site.register(Mark, MarkAdmin)
