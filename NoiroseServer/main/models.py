from django.db import models

# Create your models here.

# 사운드 센서 층간소음 측정
class Sound_Level(models.Model):
    place = models.CharField(max_length=30)       # 센서 설치 장소
    value = models.FloatField()                   # 센서 값 ( dB(A) )
    created_at = models.DateTimeField()           # 측정 날짜-시간



# 층간소음 녹음 파일
class Sound_File(models.Model):
    place = models.CharField(max_length=30)       # 녹음 장소 ( 센서 설치 장소와 동일 )
    file_name = models.CharField(max_length=40)                # 녹음된 파일 명
    created_at = models.DateTimeField()           # 녹음 날짜-시간