from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import StudentSerializer
from .models import Student

# @api_view(['POST'])
# def signup(request):

#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = User.objects.get(full_name = request.data['full_name'])
#         if year_of_study := request.data.get('year_of_study'):
#             user.year_of_study = year_of_study
#         else:
#             user.year_of_study = 'Not specified'
#         if department := request.data.get('department'):
#             user.department = department
#         else:
#             user.department = 'Not specified'
#         user.email = request.data.get('email')
#         if phone_number := request.data.get('phone_number'):
#             user.phone_number = phone_number
#         else:
#             user.phone_number = 'N/A'
#         user.set_password(request.data['password'])
#         user.save()
#         token = Token.objects.create(user=user)
#         return Response({'token': token.key, 'user': serializer.data})
#     return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        student = serializer.save()
        token, _ = Token.objects.get_or_create(user=student)
        return Response({'message': 'Signup successful', 'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login(request):

    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    student = authenticate(request, email=email, password=password)
    if student is not None:
        token, _ = Token.objects.get_or_create(user=student)
        return Response({'message': 'Login successful', 'token': token.key})
    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response("passed for {}!".format(request.user.email))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({'message': 'Token is valid'})