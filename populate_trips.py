import os
import django
from datetime import datetime

# 1. Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TirianTrains.settings')
django.setup()

from trains.models import Station, Trip, Ticket

def populate():
    print("--- 1. Cleaning old data ---")
    # Delete existing data to start fresh
    Ticket.objects.all().delete()
    Trip.objects.all().delete()
    Station.objects.all().delete()

    print("\n--- 2. Creating Stations (From SQL) ---")
    stations_data = [
        (10, 'Cubao'), 
        (11, 'Ortigas'), 
        (12, 'Shaw'), 
        (13, 'Makati'), 
        (14, 'Alabang')
    ]
    
    for s_id, name in stations_data:
        Station.objects.create(id=s_id, station_name=name)
        print(f"Created Station: {name} (ID: {s_id})")

    print("\n--- 3. Creating Trips (From SQL) ---")
    trips_data = [
        (501, 10, 11, '2025-12-01', '08:00', '09:20', 150.00),
        (502, 11, 12, '2025-12-01', '09:45', '11:00', 120.00),
        (503, 12, 13, '2025-12-02', '14:00', '15:15', 130.00),
        (504, 13, 14, '2025-12-03', '10:00', '11:40', 170.00),
        (505, 11, 10, '2025-12-03', '13:30', '15:10', 180.00),
    ]

    for t_id, org, dest, date, dep, arr, cost in trips_data:
        Trip.objects.create(
            id=t_id,
            origin_id=org,
            destination_id=dest,
            schedule_date=date,
            departure_time=dep,
            arrival_time=arr,
            cost=cost
        )
        print(f"Created Trip #{t_id}")

    print("\n--- Done! Stations and Trips loaded. No tickets created. ---")

if __name__ == '__main__':
    populate()