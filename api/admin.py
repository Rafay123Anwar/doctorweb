from django.contrib import admin
from django.utils.html import format_html
from .models import Patient,Doctor,Appointment
import base64

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'full_name', 'email', 'contact_number', 'address', 'dob', 'gender', 'profile_picture_display')

    # Displaying the profile picture as a base64 image in the admin
    def profile_picture_display(self, obj):
        if obj.profile_picture:
            # Convert binary data to base64 and display the image in the admin
            image_base64 = base64.b64encode(obj.profile_picture).decode('utf-8')
            return format_html(
                '<img src="data:image/jpeg;base64,{}" width="50" height="50" />',
                image_base64
            )
        return "No Image"

    profile_picture_display.short_description = 'Profile Picture'

    # Optional: Adding search fields or filters if necessary
    search_fields = ('full_name', 'email')
    list_filter = ('gender', 'dob')  # Example: Filter by gender and dob
    
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'full_name', 'email', 'contact_number', 'specialization', 'joining_date', 'profile_picture_display')
    search_fields = ('full_name', 'email', 'specialization')
    list_filter = ('specialization', 'gender', 'joining_date')

    # Displaying the profile picture as a base64 image in the admin
    def profile_picture_display(self, obj):
        if obj.profile_picture:
            # Convert binary data to base64 and display the image in the admin
            image_base64 = base64.b64encode(obj.profile_picture).decode('utf-8')
            return format_html(
                '<img src="data:image/jpeg;base64,{}" width="50" height="50" />',
                image_base64
            )
        return "No Image"

    profile_picture_display.short_description = 'Profile Picture'

@admin.register(Appointment)    
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'appointment_date')  # Fields to display in the list
    search_fields = ('doctor__name', 'patient__name')  # Enable search by doctor or patient name
 