import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TirianTrains.settings')
django.setup()

from trains.models import Station, Trip, Ticket, Train, MaintenanceInspection, TrainSystem

def populate():
    print("--- Cleaning old data ---")
    Ticket.objects.all().delete()
    Trip.objects.all().delete()
    Station.objects.all().delete()
    MaintenanceInspection.objects.all().delete()
    Train.objects.all().delete()
    TrainSystem.objects.all().delete()

    print("\n--- 1. Creating TRAIN SYSTEMS ---")
    sys_local = TrainSystem.objects.create(
        system_name="Western Woods Loop", 
        system_type="Local", 
        is_one_way=True
    )
    sys_inter = TrainSystem.objects.create(
        system_name="Narnia Inter-Town Express", 
        system_type="Inter-town", 
        is_one_way=False
    )

    print("\n--- 2. Creating TRAINS ---")
    t1 = Train.objects.create(
        model_name="Lion Class", model_no="L-100", max_speed=120,
        no_of_seats=70, no_of_toilets=4, 
        has_food_service=True, has_reclining_seats=True
    )
    t2 = Train.objects.create(
        model_name="Witch Class", model_no="W-50", max_speed=80,
        no_of_seats=100, no_of_toilets=2, 
        has_food_service=False, has_reclining_seats=False
    )
    t3 = Train.objects.create(
        model_name="Wardrobe Class", model_no="WR-20", max_speed=60,
        no_of_seats=40, no_of_toilets=1, 
        has_food_service=False, has_reclining_seats=False
    )

    print("\n--- 3. Creating MAINTENANCE INSPECTIONS ---")
    inspections_data = [
        (t1, "M-001", "2025-01-15", "B. Ramoh", "Routine Cleaning", "Excellent"),
        (t1, "M-002", "2025-06-20", "N. Khitsu", "Brake Disc Replacement", "Good"),
        (t1, "M-003", "2025-11-05", "C. Itson", "Oil Change", "Excellent"),
        
        (t2, "M-004", "2025-02-10", "Mr. Tumnus", "Engine Check", "Fair"),
        (t2, "M-005", "2025-08-12", "Beaver Crew", "Seat Upholstery Repair", "Good"),

        (t3, "M-006", "2025-03-30", "Dwarf Team", "Wheel Alignment", "Good"),
    ]

    for train_obj, m_no, date, crew, task, cond in inspections_data:
        MaintenanceInspection.objects.create(
            train=train_obj,
            maintenance_no=m_no,
            date_completed=date,
            crew_in_charge=crew,
            task_completed=task,
            condition=cond
        )
        print(f"Logged Inspection {m_no} for {train_obj.model_name}")

    print("\n--- 4. Creating STATIONS ---")
    stations_data = [
        (10, 'Cubao', sys_local), 
        (11, 'Ortigas', sys_local), 
        (12, 'Shaw', sys_local), 
        (13, 'Makati', sys_inter), 
        (14, 'Alabang', sys_inter)
    ]

    for sid, name, system in stations_data:
        Station.objects.create(id=sid, station_name=name, train_system=system)

    print("\n--- 5. Creating TRIPS ---")
    trips_data = [
        (501, 10, 11, '2025-12-01', '08:00', '09:20', 150.00, t1),
        (502, 11, 12, '2025-12-01', '09:45', '11:00', 120.00, t2),
        (503, 12, 13, '2025-12-02', '14:00', '15:15', 130.00, t1),
        (504, 13, 14, '2025-12-03', '10:00', '11:40', 170.00, t2),
        (505, 11, 10, '2025-12-03', '13:30', '15:10', 180.00, t3),
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