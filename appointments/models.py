from django.db import models

class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    max_appointments = models.IntegerField(default=4)  

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    car_license_number = models.CharField(max_length=50)
    car_engine_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    appointment_date = models.DateField()

    def __str__(self):
        return f"{self.client.name} - {self.mechanic.name} on {self.appointment_date}"
