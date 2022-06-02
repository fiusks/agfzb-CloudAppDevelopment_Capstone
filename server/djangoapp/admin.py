from django.contrib import admin
from .models import CarMake, CarModel


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

# CarModelAdmin class


class CarModelAmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'year']
    list_filter = ['year']
    search_field = ['name', 'type']

# CarMakeAdmin class with CarModelInline


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']


# Register models here
admin.site.register(CarModel, CarModelAmin)
admin.site.register(CarMake, CarMakeAdmin)
