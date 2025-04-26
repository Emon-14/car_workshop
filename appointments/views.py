from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Mechanic, Appointment, Client
from .forms import ClientForm, AppointmentForm
from django.db.models import Count, Q
from .forms import MechanicForm


def user_panel(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        appointment_form = AppointmentForm(request.POST)

        if client_form.is_valid() and appointment_form.is_valid():
            client = client_form.save()

            
            appointment_date = appointment_form.cleaned_data['appointment_date']
            if Appointment.objects.filter(client=client, appointment_date=appointment_date).exists():
                messages.error(request, "You already have an appointment on this date.")
                return redirect('user_panel')

            
            mechanic = appointment_form.cleaned_data['mechanic']
            if Appointment.objects.filter(mechanic=mechanic, appointment_date=appointment_date).count() >= mechanic.max_appointments:
                messages.error(request, f"{mechanic.name} is fully booked. Please choose another mechanic.")
                return redirect('user_panel')

            
            appointment = appointment_form.save(commit=False)
            appointment.client = client
            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('success')

    else:
        client_form = ClientForm()
        appointment_form = AppointmentForm()

    
    mechanics = Mechanic.objects.annotate(
        available_slots=Count('appointment', filter=Q(appointment__appointment_date=request.GET.get('appointment_date', None))))

    return render(request, 'appointments/user_panel.html', {
        'client_form': client_form,
        'appointment_form': appointment_form,
        'mechanics': mechanics,
    })
def user_panel(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        appointment_form = AppointmentForm(request.POST)

        if client_form.is_valid() and appointment_form.is_valid():
            client = client_form.save()

            
            appointment_date = appointment_form.cleaned_data['appointment_date']
            if Appointment.objects.filter(client=client, appointment_date=appointment_date).exists():
                messages.error(request, "You already have an appointment on this date.")
                return redirect('user_panel')

            
            mechanic = appointment_form.cleaned_data['mechanic']
            mechanic_appointments = Appointment.objects.filter(
                mechanic=mechanic, appointment_date=appointment_date
            ).count()
            if mechanic_appointments >= mechanic.max_appointments:
                messages.error(request, f"{mechanic.name} is fully booked. Please choose another mechanic.")
                return redirect('user_panel')

            
            appointment = appointment_form.save(commit=False)
            appointment.client = client
            appointment.save()

            
            remaining_slots = mechanic.max_appointments - (mechanic_appointments + 1)

            
            return render(request, 'appointments/success.html', {
                'mechanic': mechanic,
                'remaining_slots': remaining_slots,
            })

    else:
        client_form = ClientForm()
        appointment_form = AppointmentForm()

    
    mechanics = Mechanic.objects.all()
    mechanics_with_slots = []
    for mechanic in mechanics:
        mechanic_appointments = Appointment.objects.filter(
            mechanic=mechanic, appointment_date=request.GET.get('appointment_date', None)
        ).count()
        available_slots = mechanic.max_appointments - mechanic_appointments
        mechanics_with_slots.append({
            'mechanic': mechanic,
            'available_slots': available_slots
        })

    return render(request, 'appointments/user_panel.html', {
        'client_form': client_form,
        'appointment_form': appointment_form,
        'mechanics_with_slots': mechanics_with_slots,
    })

def admin_panel(request):
    appointments = Appointment.objects.select_related('client', 'mechanic').all()
    mechanics = Mechanic.objects.all()
    return render(request, 'appointments/admin_panel.html', {
        'mechanics': mechanics,
        'appointments': appointments,
    })

def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully!")
            return redirect('admin_panel')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/edit_appointment.html', {'form': form})


def success(request):
    return render(request, 'appointments/success.html')





def add_mechanic(request):
    if request.method == 'POST':
        form = MechanicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mechanic added successfully!")
            return redirect('admin_panel')
    else:
        form = MechanicForm()
    return render(request, 'appointments/add_mechanic.html', {'form': form})


def remove_mechanic(request, pk):
    mechanic = get_object_or_404(Mechanic, pk=pk)
    mechanic.delete()
    messages.success(request, "Mechanic removed successfully!")
    return redirect('admin_panel')


def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully!")
    return redirect('admin_panel')
