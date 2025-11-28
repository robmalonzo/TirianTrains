import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TirianTrains.settings')
django.setup()

from trains.models import Station, Trip, Ticket, Train, MaintenanceInspection

def populate():
    print("--- Cleaning old data ---")
    Ticket.objects.all().delete()
    Trip.objects.all().delete()
    Station.objects.all().delete()
    Train.objects.all().delete()
    MaintenanceInspection.objects.all().delete()

    print("\n--- 1. Creating TRAINS (Full Specs) ---")
    # Train 1: The "Lion Class" (Luxury)
    t1 = Train.objects.create(
        model_name="Lion Class", model_no="L-100", max_speed=120,
        no_of_seats=70, no_of_toilets=4,
        has_reclining_seats=True, has_folding_tables=True,
        has_disability_access=True, has_luggage_storage=True,
        has_vending_machine=True, has_food_service=True
    )
    
    t2 = Train.objects.create(
        model_name="Witch Class", model_no="W-50", max_speed=80,
        no_of_seats=100, no_of_toilets=2,
        has_reclining_seats=False, has_folding_tables=False,
        has_disability_access=True, has_luggage_storage=True,
        has_vending_machine=False, has_food_service=False
    )

    print("\n--- 2. Creating MAINTENANCE LOGS ---")
    MaintenanceInspection.objects.create(
        train=t1, maintenance_no="M-001", date_completed="2025-10-01",
        crew_in_charge="B. Ramoh", task_completed="Cleaning", condition="Excellent"
    )
    MaintenanceInspection.objects.create(
        train=t2, maintenance_no="M-002", date_completed="2025-10-05",
        crew_in_charge="N. Khitsu", task_completed="Engine Check", condition="Good"
    )

    print("\n--- 3. Creating Stations & Trips ---")
    stations = [(10,'Cubao'), (11,'Ortigas'), (12,'Shaw'), (13,'Makati'), (14,'Alabang')]
    for sid, name in stations: Station.objects.create(id=sid, station_name=name)

    trips_data = [
        (501, 10, 11, '2025-12-01', '08:00', '09:20', 150.00, t1),
        (502, 11, 12, '2025-12-01', '09:45', '11:00', 120.00, t2),
        (503, 12, 13, '2025-12-02', '14:00', '15:15', 130.00, t1),
        (504, 13, 14, '2025-12-03', '10:00', '11:40', 170.00, t2),
        (505, 11, 10, '2025-12-03', '13:30', '15:10', 180.00, t1),
    ]

    for t_id, org, dest, date, dep, arr, cost, train_obj in trips_data:
        Trip.objects.create(
            id=t_id, origin_id=org, destination_id=dest,
            schedule_date=date, departure_time=dep, arrival_time=arr,
            cost=cost, train=train_obj
        )
        print(f"Created Trip #{t_id}")

if __name__ == '__main__':
    populate()