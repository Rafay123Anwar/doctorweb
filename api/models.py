from django.db import models
from django.core.exceptions import ValidationError


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, unique=True)  # Contact number (unique)
    address = models.TextField()  # Address
    dob = models.DateField()  # Date of birth
    gender = models.CharField(max_length=10)  # Gender
    profile_picture = models.BinaryField(null=True, blank=True)  # To store binary image data

    def __str__(self):
        return self.full_name


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    specialization = models.CharField(max_length=100)  # Field of specialization
    # qualifications = models.TextField()  # Qualifications or degrees
    dob = models.DateField()  # Date of birth
    gender = models.CharField(max_length=10)
    profile_picture = models.BinaryField(null=True, blank=True)  # Binary data for profile picture
    joining_date = models.DateField(auto_now_add=True)  # Joining date of the doctor

    def __str__(self):
        return self.full_name
    
    
class Staff(models.Model):
    managed_patients = models.ManyToManyField(Patient, related_name='managed_by_staff', blank=True)
    managed_doctors = models.ManyToManyField(Doctor, related_name='managed_by_staff', blank=True)

    def save(self, *args, **kwargs):
        if Staff.objects.exists() and not self.pk:
            raise ValidationError("You can only have one staff instance.")
        super().save(*args, **kwargs)

    def __str__(self):
        return "Admin Staff"
    
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # The doctor for the appointment
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # The patient booking the appointment
    appointment_date = models.DateTimeField()  # Date and time of the appointment
    

    def __str__(self):
        # Return doctor ID and patient ID along with the appointment date
        return f"Appointment with Doctor ID: {self.doctor.doctor_id} and Patient ID: {self.patient.patient_id} on {self.appointment_date}"

    class Meta:
        ordering = ['appointment_date']  # Sort appointments by date