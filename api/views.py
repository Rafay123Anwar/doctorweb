from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Patient,Doctor,Appointment
from django.utils.dateparse import parse_datetime
import base64
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def convert_image_to_base64(image_data):
    return base64.b64encode(image_data).decode('utf-8')
def home(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')


def doctorlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Query doctor by email
            doctor = Doctor.objects.get(email=email)

            # Check if the hashed password matches
            if check_password(password, doctor.password):  # Use check_password to compare the hashed password
                # Log the doctor in manually (you can use Django's session or custom login logic)
                # You can also store the doctor_id in the session if you want to track the logged-in user
                request.session['doctor_id'] = doctor.doctor_id
                return redirect('doctorprofile', doctor_id=doctor.doctor_id)  # Redirect to doctor profile page
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        except Doctor.DoesNotExist:
            messages.error(request, "Doctor not found with this email address.")

    return render(request, 'doctorlogin.html')

def doctorprofile(request, doctor_id):
    print("rafay")
    
    # Fetch the doctor using the doctor_id passed in the URL
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    print("Doctor retrieved successfully")

    image_base64 = None  # Default to None in case there's no image
    
    # Check if the doctor has a profile picture
    if doctor.profile_picture:
        image_base64 = base64.b64encode(doctor.profile_picture).decode('utf-8')
        print(f"Image Base64: {image_base64[:100]}...")  # Print part of the base64 string for debugging
    else:
        print("No profile picture found for the doctor")

    # Prepare the context for rendering the profile
    context = {
        'doctor': doctor,  # Pass the doctor object to the template
        'image_base64': image_base64,  # Pass the base64 image data to the template
    }
    
    return render(request, 'doctorprofile.html', context)

def contact(request):
    return render(request, 'contact.html')


# def DoctorSeeAppointment(request):
#     doctor_id = request.session.get('doctor_id')
#     print(doctor_id)
#     if doctor_id:
#         try:
#             # Query using patient_id instead of id
#             doctor = Doctor.objects.get(doctor_id=doctor_id)

#             # Convert profile picture to base64 if needed
#             image_base64 = None
#             if doctor.profile_picture:
#                 image_base64 = convert_image_to_base64(doctor.profile_picture)

#             context = {
#                 'doctor': doctor,
#                 'image_base64': image_base64
#             }
#             return render(request, 'DoctorSeeAppointment.html', context)
#         except Patient.DoesNotExist:
#             return redirect('doctorlogin')  # Redirect if patient does not exist
#     else:
#         return redirect('doctorlogin')


import base64

def convert_image_base64(image):
    if image:
        try:
            # Directly encode binary data to Base64
            return base64.b64encode(image).decode('utf-8')
        except Exception as e:
            print(f"Error converting image: {e}")
    return None

def DoctorSeeAppointment(request):
    doctor_id = request.session.get('doctor_id')
    if doctor_id:
        try:
            doctor = Doctor.objects.get(doctor_id=doctor_id)
            
            # Get all appointments for this doctor
            appointments = Appointment.objects.filter(doctor=doctor)

            # Process appointments to include patient profile pictures in Base64
            appointments_with_images = []
            for appointment in appointments:
                patient = appointment.patient
                image_base64 = None
                if patient.profile_picture:  # Check if the patient has a profile picture
                    image_base64 = convert_image_base64(patient.profile_picture)
                
                # Add appointment details along with Base64 image
                appointments_with_images.append({
                    'appointment': appointment,
                    'image_base64': image_base64
                })

            context = {
                'doctor': doctor,
                'appointments_with_images': appointments_with_images
            }
            return render(request, 'DoctorSeeAppointment.html', context)
        except Doctor.DoesNotExist:
            return redirect('doctorlogin')
    else:
        return redirect('doctorlogin')








def signup(request):
    if request.session.get('patient_id'):
        return redirect('patientprofile', patient_id=request.session.get('patient_id'))
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')

        # Get the uploaded image and convert it to binary
        profile_picture = request.FILES.get('profile_picture')
        profile_picture_data = None

        if profile_picture:
            profile_picture_data = profile_picture.read()

        # Validation
        # Check if email already exists
        if Patient.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})

        # Check if contact number already exists
        if Patient.objects.filter(contact_number=contact_number).exists():
            return render(request, 'signup.html', {'error': 'Contact number already registered'})

        # Check if password and confirm password match
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        # Save the data to the database
        hashed_password = make_password(password)  # Hash the password
        Patient.objects.create(
            full_name=full_name, 
            email=email, 
            password=hashed_password,
            contact_number=contact_number,  # Save contact number
            address=address,  # Save address
            dob=dob,  # Save date of birth
            gender=gender,  # Save gender
            profile_picture=profile_picture_data  # Save the binary image data
        )

        return redirect('loginpage')  # Redirect to the login page
    
    return render(request, 'signup.html')





def loginpage(request):
    # If the patient is already logged in, redirect to the appointment page
    if request.session.get('patient_id'):
        return redirect('BookAppointment')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            patient = Patient.objects.get(email=email)
            if check_password(password, patient.password):
                # Store patient ID in session after successful login
                request.session['patient_id'] = patient.patient_id

                # Convert profile picture to base64 if available
                image_base64 = None
                if patient.profile_picture:
                    image_base64 = convert_image_to_base64(patient.profile_picture)

                # Redirect to patient profile after login
                return redirect('patientprofile', patient_id=patient.patient_id)  # Updated to include patient_id in URL
            else:
                return render(request, 'loginpage.html', {'error': 'Invalid password'})
        except Patient.DoesNotExist:
            return render(request, 'loginpage.html', {'error': 'Email not registered'})

    return render(request, 'loginpage.html')


def patientprofile(request, patient_id):  # Accept patient_id as a parameter
    # Check if the patient ID is in the session, else redirect to login page
    if request.session.get('patient_id'):
        try:
            # Fetch the patient record using patient_id from the URL
            patient = Patient.objects.get(patient_id=patient_id)

            # Convert profile picture to base64 if it exists
            image_base64 = None
            if patient.profile_picture:
                image_base64 = convert_image_to_base64(patient.profile_picture)

            # Prepare the context for rendering the profile
            context = {
                'patient': patient,
                'image_base64': image_base64,
            }
            return render(request, 'patientprofile.html', context)
        except Patient.DoesNotExist:
            # If the patient ID is invalid or not found, redirect to login
            return redirect('loginpage')
    else:
        # If no patient ID is in the session, redirect to login
        return redirect('loginpage')

# def loginpage(request):
#     # If the patient is already logged in, redirect to the appointment page
#     if request.session.get('patient_id'):
#         return redirect('BookAppointment')

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             patient = Patient.objects.get(email=email)
#             if check_password(password, patient.password):
#                 # Store patient ID in session after successful login
#                 request.session['patient_id'] = patient.patient_id

#                 # Convert profile picture to base64 if available
#                 image_base64 = None
#                 if patient.profile_picture:
#                     image_base64 = convert_image_to_base64(patient.profile_picture)

#                 # Redirect to patient profile after login
#                 return redirect('patientprofile', patient_id=patient.patient_id)
#             else:
#                 return render(request, 'loginpage.html', {'error': 'Invalid password'})
#         except Patient.DoesNotExist:
#             return render(request, 'loginpage.html', {'error': 'Email not registered'})

#     return render(request, 'loginpage.html')




# def patientprofile(request):
#     # Retrieve patient ID from session
#     patient_id = request.session.get('patient_id')
    
#     if patient_id:  # Check if patient_id exists in the session
#         try:
#             # Fetch the patient record using patient_id
#             patient = Patient.objects.get(patient_id=patient_id)
            
#             # Convert profile picture to base64 if it exists
#             image_base64 = None
#             if patient.profile_picture:
#                 image_base64 = convert_image_to_base64(patient.profile_picture)
            
#             # Prepare the context for rendering the profile
#             context = {
#                 'patient': patient,
#                 'image_base64': image_base64,
#             }
#             return render(request, 'patientprofile.html', context)
#         except Patient.DoesNotExist:
#             # If the patient ID is invalid or not found, redirect to login
#             return redirect('loginpage')
#     else:
#         # If no patient ID is in the session, redirect to login
#         return redirect('loginpage')




from django.contrib import messages
from django.utils import timezone
from datetime import datetime

from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, Doctor, Appointment

def BookAppointment(request):
    # Retrieve patient_id from session
    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('login')  # Redirect to login if session is missing

    try:
        # Get patient details using patient_id
        patient = Patient.objects.get(patient_id=patient_id)

        # Fetch all unique specializations
        specializations = Doctor.objects.values_list('specialization', flat=True).distinct()

        # Check for specialization filter in GET or POST request
        selected_specialization = request.GET.get('specialization') or request.POST.get('specialization')

        # Populate the doctors list based on the selected specialization
        doctors = []
        # if selected_specialization:
        #     doctors = Doctor.objects.filter(specialization__iexact=selected_specialization) 
        #     if not doctors:
        #         messages.warning(request, f"No doctors found for specialization '{selected_specialization}'.")
        if selected_specialization:
            doctors = Doctor.objects.filter(specialization__iexact=selected_specialization)
            if not doctors:
                messages.warning(request, f"No doctors found for specialization '{selected_specialization}'.")
            else:
                print("Doctors available for this specialization:")
                for doctor in doctors:
                    print(f"Doctor ID: {doctor.doctor_id}, Name: {doctor.full_name}")


        # Handle POST request for appointment booking
        if request.method == "POST":
            doctor_id = request.POST.get('doctor')
            appointment_date = request.POST.get('date')

            # Debugging statements
            print(f"POST data: {request.POST}")
            print(f"Doctors in context: {doctors}")
            print(f"Doctor ID: {doctor_id}, Appointment Date: {appointment_date}")
            print("debug")
            print("Doctors in POST context:")
            for doctor in doctors:
                print(f"Doctor ID: {doctor.doctor_id}, Name: {doctor.full_name}")

            if doctor_id and appointment_date:
                try:
                    # Validate doctor and appointment date
                    doctor = Doctor.objects.get(doctor_id=doctor_id)
                    if isinstance(appointment_date, str):
                        appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()

# Ensure the date is not in the past
                    if appointment_date < datetime.now().date():
                        messages.error(request, "You cannot book an appointment for a past date.")
                    else:
                        # Save the appointment
                        Appointment.objects.create(
                            doctor=doctor,
                            patient=patient,
                            appointment_date=appointment_date,
                        )
                        messages.success(request, "Appointment booked successfully!")
                        return redirect('BookAppointment')
                except Doctor.DoesNotExist:
                    messages.error(request, "The selected doctor does not exist.")
                except ValueError:
                    messages.error(request, "Invalid date format.")
            else:
                # Check missing fields and provide feedback
                if not doctor_id:
                    print("Missing: Doctor ID")
                if not appointment_date:
                    print("Missing: Appointment Date")
                messages.error(request, "Please fill in all required fields.")

        # Context for rendering the template
        context = {
            'patient': patient,
            'specializations': specializations,
            'Doctors': doctors,
            'selected_specialization': selected_specialization,
        }
        return render(request, 'BookAppointment.html', context)

    except Patient.DoesNotExist:
        messages.error(request, "Patient not found. Please log in again.")
        return redirect('login')





from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    # Clear any session data if necessary
    if 'patient_id' in request.session:
        del request.session['patient_id']
    
    # Log out the user
    logout(request)
    
    # Redirect to the login page
    return redirect('home') 