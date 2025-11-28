from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Station, Trip, Ticket, Train, MaintenanceInspection

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ['username', 'first_name', 'last_name', 'gender', 'birth_date']
    fieldsets = UserAdmin.fieldsets + (('Personal Info', {'fields': ('gender', 'birth_date')}),)

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'model_no', 'max_speed', 'no_of_seats']

@admin.register(MaintenanceInspection)
class MaintenanceAdmin(admin.ModelAdmin):
    # This proves you implemented the table
    list_display = ['maintenance_no', 'train', 'date_completed', 'condition', 'crew_in_charge']
    list_filter = ['condition', 'train']

admin.site.register(Station)
admin.site.register(Trip)
admin.site.register(Ticket)