from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Station, Trip, Ticket, Train, MaintenanceInspection, TrainSystem

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ['username', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (('Personal Info', {'fields': ('gender', 'birth_date')}),)

admin.site.register(TrainSystem) 
admin.site.register(Station)
admin.site.register(Trip)
admin.site.register(Ticket)
admin.site.register(Train)
admin.site.register(MaintenanceInspection)