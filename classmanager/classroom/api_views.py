from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import (
    User, Student, Teacher, StudentMarks, ClassNotice, 
    ClassAssignment, SubmitAssignment, MessageToTeacher, StudentsInClass
)
from .serializers import (
    UserSerializer, StudentSerializer, TeacherSerializer, StudentMarksSerializer,
    ClassNoticeSerializer, ClassAssignmentSerializer, SubmitAssignmentSerializer,
    MessageToTeacherSerializer
)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        user_type = 'student' if user.is_student else 'teacher' if user.is_teacher else 'unknown'
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'user_type': user_type
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def student_signup(request):
    try:
        # Extract user data from request
        username = request.data.get('username')
        password = request.data.get('password1')
        name = request.data.get('name')
        roll_no = request.data.get('roll_no')
        email = request.data.get('email')
        phone = request.data.get('phone')
        
        # Validate data
        if not all([username, password, name, roll_no, email]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create user and student
        user = User.objects.create_user(
            username=username,
            password=password,
            is_student=True
        )
        
        student = Student.objects.create(
            user=user,
            name=name,
            roll_no=roll_no,
            email=email,
            phone=phone
        )
        
        return Response({
            'success': True,
            'message': 'Student account created successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Error creating student account: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def teacher_signup(request):
    try:
        # Extract user data from request
        username = request.data.get('username')
        password = request.data.get('password1')
        name = request.data.get('name')
        subject_name = request.data.get('subject_name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        
        # Validate data
        if not all([username, password, name, subject_name, email]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create user and teacher
        user = User.objects.create_user(
            username=username,
            password=password,
            is_teacher=True
        )
        
        teacher = Teacher.objects.create(
            user=user,
            name=name,
            subject_name=subject_name,
            email=email,
            phone=phone
        )
        
        return Response({
            'success': True,
            'message': 'Teacher account created successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Error creating teacher account: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    serializer = StudentSerializer(student)
    return Response(serializer.data)

@api_view(['PUT'])
def update_student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    serializer = StudentSerializer(student, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_teacher_profile(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    serializer = TeacherSerializer(teacher)
    return Response(serializer.data)

@api_view(['PUT'])
def update_teacher_profile(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    serializer = TeacherSerializer(teacher, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_student_marks(request, pk):
    student = get_object_or_404(Student, pk=pk)
    marks = StudentMarks.objects.filter(student=student)
    serializer = StudentMarksSerializer(marks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_student_notices(request, pk):
    student = get_object_or_404(Student, pk=pk)
    notices = student.class_notice.all()
    serializer = ClassNoticeSerializer(notices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_student_assignments(request, pk):
    student = get_object_or_404(Student, pk=pk)
    assignments = student.student_assignment.all()
    serializer = ClassAssignmentSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_teacher_assignments(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    assignments = teacher.teacher_assignment.all()
    serializer = ClassAssignmentSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_teacher_class_students(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    students = teacher.class_students.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_student_to_class(request, teacher_pk, student_pk):
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    student = get_object_or_404(Student, pk=student_pk)
    
    # Check if student is already in class
    if StudentsInClass.objects.filter(teacher=teacher, student=student).exists():
        return Response({'error': 'Student already in class'}, status=status.HTTP_400_BAD_REQUEST)
    
    StudentsInClass.objects.create(teacher=teacher, student=student)
    return Response({'success': True}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_all_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def upload_assignment(request):
    # In a full implementation, you would process the file upload
    # Return placeholder response
    return Response({'message': 'Assignment upload endpoint working'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def submit_assignment(request, assignment_pk):
    # Similar to upload_assignment
    return Response({'message': 'Assignment submission endpoint working'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_student_marks(request, student_pk):
    # Process adding marks
    return Response({'message': 'Add marks endpoint working'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_notice(request):
    # Process adding notice
    return Response({'message': 'Add notice endpoint working'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def send_message_to_teacher(request, teacher_pk):
    # Process sending message
    return Response({'message': 'Send message endpoint working'}, status=status.HTTP_200_OK)