from django.db import models

# Create your models here.
class user_management(models.Model):
    userid = models.CharField(max_length=32,
                                verbose_name='사용자 아이디')
    useremail = models.EmailField(max_length=32,
                                  verbose_name='사용자 이메일')
    userpassword = models.CharField(max_length=32,
                                verbose_name='사용자 비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')
    fail_account_count = models.IntegerField(default = 0, verbose_name='로그인 실패 횟수')
    login_judge = models.CharField(max_length=16,
                                default='success', verbose_name='잠금 상태')
    
    def __str__(self):
        return self.userid

    class Meta:
        db_table = 'user_management'
        verbose_name = '사용자 관리'
        verbose_name_plural = '사용자 관리'
