from rest_framework import serializers
from .models import User, Student, Teacher, StudentMarks, ClassNotice, ClassAssignment, SubmitAssignment, MessageToTeacher

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_student', 'is_teacher']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = ['user', 'name', 'roll_no', 'email', 'phone', 'student_profile_pic']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['user', 'name', 'subject_name', 'email', 'phone', 'teacher_profile_pic']

class StudentMarksSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    
    class Meta:
        model = StudentMarks
        fields = ['id', 'subject_name', 'marks_obtained', 'maximum_marks', 'teacher_name']

class ClassNoticeSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    
    class Meta:
        model = ClassNotice
        fields = ['id', 'message', 'created_at', 'teacher_name']

class ClassAssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    
    class Meta:
        model = ClassAssignment
        fields = ['id', 'assignment_name', 'assignment', 'created_at', 'teacher_name']

class SubmitAssignmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    assignment_name = serializers.CharField(source='submitted_assignment.assignment_name', read_only=True)
    
    class Meta:
        model = SubmitAssignment
        fields = ['id', 'submit', 'created_at', 'student_name', 'assignment_name']

class MessageToTeacherSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    
    class Meta:
        model = MessageToTeacher
        fields = ['id', 'message', 'created_at', 'student_name']