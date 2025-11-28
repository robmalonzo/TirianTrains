from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime, date, timedelta

class Customer(AbstractUser):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    def __str__(self): return self.username

class Station(models.Model):
    station_name = models.CharField(max_length=100)
    def __str__(self): return self.station_name

class Train(models.Model):
    model_name = models.CharField(max_length=50) 
    model_no = models.CharField(max_length=20)   
    max_speed = models.IntegerField(help_text="km/h")
    no_of_seats = models.IntegerField(default=50)       
    no_of_toilets = models.IntegerField(default=2)      
    
    has_reclining_seats = models.BooleanField(default=False)
    has_folding_tables = models.BooleanField(default=False)  
    has_disability_access = models.BooleanField(default=False)
    has_luggage_storage = models.BooleanField(default=False)  
    has_vending_machine = models.BooleanField(default=False)  
    has_food_service = models.BooleanField(default=False)

    def __str__(self): return f"{self.model_name} ({self.model_no})"

class MaintenanceInspection(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='inspections')
    maintenance_no = models.CharField(max_length=20, unique=True)
    date_completed = models.DateField()
    crew_in_charge = models.CharField(max_length=100)
    task_completed = models.TextField()
    condition = models.CharField(max_length=50) 

    def __str__(self):
        return f"Insp #{self.maintenance_no} - {self.train.model_no}"

class Trip(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='trips', null=True)
    origin = models.ForeignKey(Station, related_name='departures', on_delete=models.CASCADE)
    destination = models.ForeignKey(Station, related_name='arrivals', on_delete=models.CASCADE)
    schedule_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def duration(self):
        dummy_date = date.today()
        start = datetime.combine(dummy_date, self.departure_time)
        end = datetime.combine(dummy_date, self.arrival_time)
        if end < start: end += timedelta(days=1)
        diff = end - start
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        return f"{hours} hr {minutes:02d} min"

    def __str__(self): return f"{self.origin} -> {self.destination}"

class Ticket(models.Model):
    SEAT_CLASSES = [('Economy', 'Economy'), ('Business', 'Business'), ('First', 'First Class')]
    TRIP_TYPES = [('One-Way', 'One-Way'), ('Round-Trip', 'Round-Trip')]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    date_created = models.DateTimeField(auto_now_add=True)
    trips = models.ManyToManyField(Trip, blank=True)
    ticket_number = models.PositiveIntegerField(default=1)
    
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASSES, default='Economy')
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPES, default='One-Way')

    @property
    def total_cost(self): return sum(trip.cost for trip in self.trips.all())

    def save(self, *args, **kwargs):
        if not self.pk:
            count = Ticket.objects.filter(customer=self.customer).count()
            self.ticket_number = count + 1
        super().save(*args, **kwargs)

    def __str__(self): return f"Ticket #{self.ticket_number}"