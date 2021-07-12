from django.db import models

# Create your models here.

class Dsuser(models.Model):
    userid = models.CharField(max_length=128, verbose_name='아이디')
    email = models.EmailField(verbose_name='이메일')

    password = models.CharField(max_length=128, verbose_name='비밀번호')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='가입일')

    def __str__(self):
        return self.userid

    class Meta:
        db_table = 'djangostagram_dsuser'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
