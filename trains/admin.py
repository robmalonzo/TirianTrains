from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Station, Trip, Ticket

# 1. Register the Custom Customer Model
# We use a custom configuration to show the new fields (birth_date, gender) in the admin
@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    model = Customer
    # Add these fields to the user list view
    list_display = ['username', 'email', 'first_name', 'last_name', 'gender', 'birth_date', 'is_staff']
    
    # Add the custom fields to the "Edit User" page
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Info', {'fields': ('gender', 'birth_date')}),
    )

# 2. Register Station
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['station_name'] 

# 3. Register Trip
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    # Display origin, destination, date, and cost in the list
    list_display = ['origin', 'destination', 'schedule_date', 'departure_time', 'cost'] 
    list_filter = ['schedule_date', 'origin', 'destination'] # Adds sidebar filters

# 4. Register Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'ticket_number', 'date_created', 'total_cost'] 
    list_filter = ['date_created']