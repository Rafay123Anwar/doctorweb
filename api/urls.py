from django.urls import path
from . import views,adminviews

urlpatterns = [
    path('', views.home,name='home'),
    path('about/', views.about,name='about'),
    path('BookAppointment/', views.BookAppointment,name='BookAppointment'),
    path('contact/', views.contact,name='contact'),
    path('doctorlogin/', views.doctorlogin,name='doctorlogin'),
    # path('doctorprofile/', views.doctorprofile,name='doctorprofile'),
    path('DoctorSeeAppointment/', views.DoctorSeeAppointment,name='DoctorSeeAppointment'),
    path('loginpage/', views.loginpage,name='loginpage'),
    # path('patientprofile/', views.patientprofile,name='patientprofile'),
    path('signup/', views.signup,name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('doctorprofile/<int:doctor_id>/', views.doctorprofile, name='doctorprofile'),
    

    path('adminpage/', adminviews.adminpage, name='adminpage'),
    path('adminloginpage/', adminviews.adminloginpage, name='adminloginpage'),
    # path('adminlogout/', adminviews.adminlogout_view, name='adminlogout'),
    path('adminlogout/', adminviews.adminlogout_view, name='adminlogout_view'),
    # path('adminloginpage/', adminviews.adminloginpage, name='adminloginpage'),
    # path('adminpage/', adminviews.adminpage, name='adminpage'),
    path('viewpatient/', adminviews.viewpatient, name='viewpatient'),
    path('viewdoctor/', adminviews.viewdoctor, name='viewdoctor'),
    path('signupdoctor/', adminviews.signupdoctor, name='signupdoctor'),
    path('patientprofile/<int:patient_id>/', views.patientprofile, name='patientprofile'),
    # path('doctor/profile/<int:doctor_id>/', adminviews.visit_profile_doctor, name='visit_profile_doctor'),
    path('visitdoctorprofile/<int:doctor_id>/', adminviews.visit_profile_doctor, name='visit_profile_doctor'),
    path('visitDoctorSeeAppointment/<int:doctor_id>/', adminviews.visitDoctorSeeAppointment, name='visitDoctorSeeAppointment'),
    path('doctor/delete/<int:doctor_id>/', adminviews.delete_doctor, name='delete_doctor'),
    # path('viewdoctor/', adminviews.delete_doctor, name='delete_doctor'),
    # path('patientprofile/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
]