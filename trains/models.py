from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Customer(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return self.username

class Station(models.Model):
    station_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.station_name

class Trip(models.Model):
    origin = models.ForeignKey(Station, related_name='departures', on_delete=models.CASCADE)
    destination = models.ForeignKey(Station, related_name='arrivals', on_delete=models.CASCADE)
    schedule_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.origin} -> {self.destination} ({self.schedule_date})"

class Ticket(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    date_created = models.DateTimeField(auto_now_add=True) 
    trips = models.ManyToManyField(Trip, blank=True) 
    
    ticket_number = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return sum(trip.cost for trip in self.trips.all()) 

    def save(self, *args, **kwargs):
        if not self.pk: 
            previous_tickets_count = Ticket.objects.filter(customer=self.customer).count()
            self.ticket_number = previous_tickets_count + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket #{self.ticket_number} - {self.customer.username}"