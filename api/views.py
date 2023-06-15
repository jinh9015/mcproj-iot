from django.shortcuts import render
from django.contrib.auth import login, authenticate

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated            # 토큰 인증 및 권한 확인을 위한 함수
from rest_framework.authtoken.models import Token                                           # 토큰 기반의 로그인에서 사용, 토큰 검사를 수행한다.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication        # Django에서 기본적으로 사용되는 csrf_token를 BasicAuthentication은 수행하지 않음. CSRF 토큰검사 비활성화
from rest_framework.authentication import TokenAuthentication              

from common.models import CustomUser, CustomUserManager
from main.models import Sound_Level, Sound_File
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, SoundLevelSerializer, SoundFileSerializer

# Create your views here.

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_staff :
            users = CustomUser.objects.all()               # 모든 사용자 데이터를 가져오기
            serializer = UserSerializer(users, many=True)  # 사용자를 직렬화

            return Response(serializer.data)                   # 직렬화된 사용자 데이터를 응답에 포함
        else:  # 슈퍼유저가 아니라면, 접근 거부 메시지를 반환
            return Response({"detail": "관리자 권한이 필요합니다."}, status=403)
    

# API 서버를 통한 회원가입 함수
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer  # 바로 지정

    def get_serializer_class(self):
        return UserRegisterSerializer
    

class UserLoginView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            response = Response({"token": token.key}, status=200)
            response.set_cookie('auth-token', token.key)
            return response
        
        return Response(serializer.errors, status=401)
        
    def get(self, request, format=None):
        if request.user.is_staff :
            users = CustomUser.objects.userid()               # 모든 사용자 데이터를 가져오기
            serializer = UserSerializer(users, many=True)  # 사용자를 직렬화

            return Response(serializer.data)                   # 직렬화된 사용자 데이터를 응답에 포함
        else:  # 슈퍼유저가 아니라면, 접근 거부 메시지를 반환
            return Response({"detail": "관리자 권한이 필요합니다."}, status=403)    
        
        
class SoundLevelViewSet(viewsets.ModelViewSet):
    queryset = Sound_Level.objects.all().order_by('-id')        # ID 정렬
    serializer_class = SoundLevelSerializer                   # 데시벨 데이터에 대한 직렬화 처리

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        queryset = Sound_Level.objects.all().order_by('id')
        if queryset.count() >= 20:                         # 데시벨 데이터 생성시, 20개 이상이 되면
            queryset.first().delete()                     # 가장 먼저 만들어진 데이터부터 삭제
        return response
    


class SoundFileViewSet(viewsets.ModelViewSet):
    queryset = Sound_File.objects.all().order_by('-id')        # ID 정렬
    serializer_class = SoundFileSerializer                   # 녹음파일 데이터에 대한 직렬화 처리

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        queryset = Sound_File.objects.all().order_by('id')
        if queryset.count() >= 20:                         # 녹음파일 데이터 생성시, 20개 이상이 되면
            queryset.first().delete()                     # 가장 먼저 만들어진 데이터부터 삭제
        return response