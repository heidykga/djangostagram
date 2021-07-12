from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=128,
                             verbose_name='제목')
    writer = models.ForeignKey('dsuser.Dsuser', on_delete=models.CASCADE,
                            verbose_name='작성자')
    image = models.CharField(max_length=256, verbose_name='이미지 주소')
    contents = models.TextField(verbose_name='내용')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='작성일')
    tags = models.ManyToManyField('tag.Tag', verbose_name='태그')


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'djangostragram_post'
        verbose_name = '포스트'
        verbose_name_plural = '포스트'


    
                                
