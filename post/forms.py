from django import forms
from .models import Post

class PostForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PostForm, self).__init__(*args, **kwargs)

    title = forms.CharField(
        error_messages={
            'required': '제목을 입력해주세요.'
        },
        widget=forms.Textarea, label="제목")

    image = forms.CharField(
        error_messages={
            'required': '이미지 주소를 입력해주세요.'
        },
        max_length=128, label="이미지 주소")
    contents = forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요.'
        },
        widget=forms.Textarea, label="내용")
    tags = forms.CharField(
        required=False, label="태그")

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        image = cleaned_data.get('image')
        contents = cleaned_data.get('contents')
        tags = cleaned_data.get('tags').split(',')

        if not (title and image and contents):
            self.add_error('title', '값이 없습니다')
            self.add_error('image', '값이 없습니다')
            self.add_error('contents', '값이 없습니다')
    