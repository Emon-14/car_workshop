from django import forms
from .models import Appointment, Client
from datetime import date

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'address', 'phone', 'car_license_number', 'car_engine_number']
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean_car_engine_number(self):
        car_engine_number = self.cleaned_data.get('car_engine_number')
        if not car_engine_number.isdigit():
            raise forms.ValidationError("Car Engine Number must contain only digits.")
        return car_engine_number
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'mechanic']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        if appointment_date < date.today():
            raise forms.ValidationError("The appointment date cannot be in the past.")
        return appointment_date
    
from .models import Mechanic

class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['name', 'specialization', 'max_appointments']