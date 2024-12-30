from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from .models import Patient,Doctor,Appointment
import base64
from django.shortcuts import get_object_or_404, redirect

def viewdoctor(request):
    return render(request,'viewdoctor.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def adminloginpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Correct email and password for admin login
        if email == "admin@gmail.com" and password == "admin":
            # Get the 'next' parameter from the URL query string, if it exists
            next_url = request.GET.get('next', '/adminpage/')
            return redirect(next_url)  # Redirect to the 'next' URL or default to '/adminpage/'

        else:
            # Return an error if the login fails
            return render(request, 'adminloginpage.html', {'error': 'Invalid email or password'})
    
    return render(request, 'adminloginpage.html')

# @login_required(login_url='adminloginpage')  # Ensure only logged-in users can access this page
def adminpage(request):
    # Your admin page view logic
    return render(request, 'adminpage.html')

def viewpatient(request):
    patients_list = Patient.objects.all()

    for patient in patients_list:
        # print(patient.patient_id)
        if patient.profile_picture:  # Check if a profile picture exists
            # Directly base64 encode the binary data
            patient.image_base64 = base64.b64encode(patient.profile_picture).decode('utf-8')
            # print(f"Encoded image for patient {patient.patient_id}: {patient.image_base64[:100]}...") 
        else:
            patient.image_base64 = None  # Handle missing images gracefully

    return render(request, 'viewpatient.html', {'patients': patients_list})


def signupdoctor(request):
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        Specialist = request.POST.get('Specialist')

        profile_picture = request.FILES.get('profile_picture')
        profile_picture_data = None

        if profile_picture:
            profile_picture_data = profile_picture.read()


        if Doctor.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})

        # Check if contact number already exists
        if Doctor.objects.filter(contact_number=contact_number).exists():
            return render(request, 'signup.html', {'error': 'Contact number already registered'})

        # Check if password and confirm password match
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        # Save the data to the database
        hashed_password = make_password(password)  # Hash the password
        Doctor.objects.create(
            full_name=full_name, 
            email=email, 
            password=hashed_password,
            contact_number=contact_number,  # Save contact number
            address=address,  # Save address
            dob=dob,  # Save date of birth
            gender=gender,  # Save gender
            specialization=Specialist,
            profile_picture=profile_picture_data   # Save the binary image data
        )

        return redirect('viewdoctor') 
    return render(request,'signupdoctor.html')



def viewdoctor(request):
    doctor_list = Doctor.objects.all()

    for doctor in doctor_list:
        # print(doctor.doctor_id)
        if doctor.profile_picture:  # Check if a profile picture exists
            # Directly base64 encode the binary data
            doctor.image_base64 = base64.b64encode(doctor.profile_picture).decode('utf-8')
            # print(f"Encoded image for patient {doctor.doctor_id}: {doctor.image_base64[:100]}...") 
        else:
            doctor.image_base64 = None  

    return render(request, 'viewdoctor.html', {'doctors': doctor_list})

    
    
    
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    if request.method == "POST":
        doctor.delete()
        messages.success(request, "Doctor deleted successfully.")
        return redirect('viewdoctor')  # Replace 'view_doctors' with the URL pattern name for your doctor list page.
    return render(request, 'viewdoctor.html', {'doctor': doctor})




def convert_image_base64(image_binary):
    """Converts binary image data to Base64 string."""
    if image_binary:
        try:
            return base64.b64encode(image_binary).decode('utf-8')
        except Exception as e:
            print(f"Error converting image: {e}")
    return None


def visit_profile_doctor(request, doctor_id):
    # Fetch the doctor by ID
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    
    # Convert profile picture to Base64 if it exists
    image_base64 = convert_image_base64(doctor.profile_picture) if doctor.profile_picture else None
    
    context = {
        'doctor': doctor,
        'image_base64': image_base64
    }
    return render(request, 'visitdoctorprofile.html', context)


def visitDoctorSeeAppointment(request, doctor_id):
    # Fetch the doctor by ID
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    
    # Fetch all appointments for the doctor
    appointments = Appointment.objects.filter(doctor=doctor)

    # Process appointments to include patient profile pictures as Base64
    appointments_with_images = []
    for appointment in appointments:
        patient = appointment.patient
        image_base64 = convert_image_base64(patient.profile_picture) if patient.profile_picture else None

        # Add appointment details along with Base64 image
        appointments_with_images.append({
            'appointment': appointment,
            'image_base64': image_base64
        })

    context = {
        'doctor': doctor,
        'appointments_with_images': appointments_with_images
    }
    return render(request, 'visitDoctorSeeAppointment.html', context)



from django.contrib.auth import logout
from django.shortcuts import redirect


def adminlogout_view(request):
    # Log out the user
    logout(request)
    # Redirect to the login page
    return redirect('adminloginpage')