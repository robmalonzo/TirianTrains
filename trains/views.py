from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Ticket, Trip
from .forms import CustomerSignUpForm

def signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ticket_list')
    else:
        form = CustomerSignUpForm()
    return render(request, 'trains/signup.html', {'form': form})

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(customer=request.user).order_by('-date_created')
    return render(request, 'trains/ticket_list.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    ticket = Ticket.objects.create(customer=request.user)
    return redirect('manage_trips', ticket_id=ticket.id)

@login_required
def manage_trips(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, customer=request.user)
    all_trips = Trip.objects.all().order_by('schedule_date')

    if request.method == "POST":
        trip_id = request.POST.get('trip_id')
        trip = get_object_or_404(Trip, id=trip_id)
        
        if 'add' in request.POST:
            ticket.trips.add(trip)
        elif 'remove' in request.POST:
            ticket.trips.remove(trip)
        
        return redirect('manage_trips', ticket_id=ticket.id)

    context = {
        'ticket': ticket,
        'all_trips': all_trips,
        'selected_trip_ids': ticket.trips.values_list('id', flat=True)
    }
    return render(request, 'trains/manage_trips.html', context)