from django.urls import path
from . import api_views

urlpatterns = [
    path('auth/login', api_views.login_view, name='api_login'),
    path('auth/signup/student', api_views.student_signup, name='api_student_signup'),
    path('auth/signup/teacher', api_views.teacher_signup, name='api_teacher_signup'),
    
    path('students/<int:pk>', api_views.get_student_profile, name='api_student_profile'),
    path('students/<int:pk>/update', api_views.update_student_profile, name='api_update_student_profile'),
    path('teachers/<int:pk>', api_views.get_teacher_profile, name='api_teacher_profile'),
    path('teachers/<int:pk>/update', api_views.update_teacher_profile, name='api_update_teacher_profile'),
    
    path('students/<int:pk>/marks', api_views.get_student_marks, name='api_student_marks'),
    path('students/<int:pk>/notices', api_views.get_student_notices, name='api_student_notices'),
    path('students/<int:pk>/assignments', api_views.get_student_assignments, name='api_student_assignments'),
    path('teachers/<int:pk>/assignments', api_views.get_teacher_assignments, name='api_teacher_assignments'),
    
    path('teachers/<int:pk>/class-students', api_views.get_teacher_class_students, name='api_class_students'),
    path('teachers/<int:teacher_pk>/add-student/<int:student_pk>', api_views.add_student_to_class, name='api_add_student_to_class'),
    
    path('students', api_views.get_all_students, name='api_all_students'),
    path('teachers', api_views.get_all_teachers, name='api_all_teachers'),
    
    path('assignments/upload', api_views.upload_assignment, name='api_upload_assignment'),
    path('assignments/<int:assignment_pk>/submit', api_views.submit_assignment, name='api_submit_assignment'),
    
    path('students/<int:student_pk>/add-marks', api_views.add_student_marks, name='api_add_student_marks'),
    path('notices/add/', api_views.add_notice, name='api_add_notice'),
    path('teachers/<int:teacher_pk>/message', api_views.send_message_to_teacher, name='api_send_message'),
]