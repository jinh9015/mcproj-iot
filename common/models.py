from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class CustomUserManager(UserManager) :
    def create_user(self, userid, password, email, name, apartment, dong, ho):             # 일반 유저 생성. 유저 생성 시 필요한 매개변수 순서 확인할 것!(다른 함수 생성 시 입력순서 중요)
        if not userid :
            raise ValueError("아이디는 필수항목입니다.")
        if not name :
            raise ValueError("이름은 필수항목입니다.")
        if not apartment :
            raise ValueError("아파트명은 필수항목입니다.")
        if not dong :
            raise ValueError("주소(**동)는 필수항목입니다.")
        if not ho :
            raise ValueError("주소(**호)는 필수항목입니다.")

        email = self.normalize_email(email)                                             # 이메일은 이메일 형식으로 변환
        user = self.model(userid=userid, name=name, email=email, apartment=apartment, dong=dong, ho=ho)    # 유저 생성시 입력한 정보를 각각 커스텀 유저의 정보란에 집어넣기 (데이터 입력) 
        user.set_password(password)                                                     # 입력받은 정보를 password 로 설정
        user.is_active = True                                   # 유저 활성화 
        user.save(using=self._db)                               # db에 저장

        return user                                            # 유저 생성
    

    def create_superuser(self, userid, password=None, **extra_fields):             # 슈퍼유저 생성
        extra_fields.setdefault('email', '')
        extra_fields.setdefault('name', '')
        extra_fields.setdefault('apartment', '')                 
        extra_fields.setdefault('dong', 'A')
        extra_fields.setdefault('ho', '')                                # 커스텀유저 모델에서 만든 필드들을 슈퍼유저 생성시에 입력할 수 있게끔 해줌.

        if extra_fields.get('email') == '':
            raise ValueError('이메일은 필수항목입니다.')
        if extra_fields.get('name') == '':
            raise ValueError('이름은 필수항목입니다.')
        if extra_fields.get('apartment') == '':
            raise ValueError('아파트명은 필수항목입니다.')
        if extra_fields.get('dong') not in ('A', 'B', 'C', 'D', 'E'):
            raise ValueError('동은 필수항목이며, 선택지 중 하나를 입력해야 합니다.')
        if extra_fields.get('ho') == '':
            raise ValueError('주소(**호)는 필수항목이며, 0~9999 사이의 값을 입력해야 합니다.')        # 입력받은 값이 없으면 필수로 다시 입력하도록 함
            
        user = self.create_user (userid=userid, password=password, **extra_fields)     # 유저 생성시 입력한 정보를 각각 커스텀 유저의 정보란에 집어넣기 (데이터 입력) 
        user.is_superuser = True
        user.is_staff = True                                  # 슈퍼유저 및 스태프 권한 부여.
        user.save(using=self._db)

        return user

class CustomUser(AbstractBaseUser, PermissionsMixin) :
    userid = models.CharField(max_length = 15, unique=True)
    email = models.EmailField(blank=False, unique=True, default='')
    name = models.CharField(max_length=15)         # 세대주 이름           ## 필수!!! 아파트명, 세대주, 동, 호수
    apartment = models.CharField(max_length = 40, default='아파트명')          # 아파트이름 -> 관리자가 설정
    DONG_CHOICES = (
        ('A', 'A동'),
        ('B', 'B동'),
        ('C', 'C동'),
        ('D', 'D동'),
        ('E', 'E동'),
    )                               
    dong = models.CharField(max_length=20, choices=DONG_CHOICES, default='A')
    ho = models.CharField(blank=False, unique=True, max_length=4, default='0000')             # 커스텀 유저 모델에 사용할 필드들. userid 와 email 은 필수사항.

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'userid'                         # 장고에서 기본적으로 username -> 아이디 로 인식하는 것을 커스텀유저에서 만든 userid 로 바꿔줌
    REQUIRED_FIELDS = ['email', 'name', 'apartment', 'dong', 'ho']

    class Meta :
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'