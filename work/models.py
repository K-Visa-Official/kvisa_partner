from django.db import models
from user.models import User
from datetime import datetime
import uuid

def at_icon_path(instance, filename):
    datestamp = datetime.now().strftime('%Y%m%d')
    unique_filename = f"{uuid.uuid4().hex}_{filename}"  # UUID 추가
    return f'media/detail/{datestamp}/{unique_filename}'

def at_icon_second(instance, filename):
    datestamp = datetime.now().strftime('%Y%m%d')
    unique_filename = f"{uuid.uuid4().hex}_{filename}"  # UUID 추가
    return f'media/detail_second/{datestamp}/{unique_filename}'
    
class Work(models.Model):
    LA = [(0, "ko"), (1, "ch")]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="works")
    language = models.IntegerField(choices=LA, null=False, verbose_name="언어")
    choice = models.CharField(verbose_name="업무선택", max_length=200, null=True)
    work_detail = models.TextField(verbose_name="세부정보")

    detail = models.FileField(upload_to=at_icon_path, blank=True, default="상세화면 이미지", verbose_name="상세화면 이미지")
    detail_second = models.FileField(upload_to=at_icon_second, blank=True, default="상세화면 이미지", verbose_name="상세화면 이미지")
    order = models.IntegerField(verbose_name="업무순수" , default=0)

class Question(models.Model):
    AT = [(0, "short_subjective"), (1, "single"), (2, "multiple")]

    id = models.AutoField(primary_key=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField(verbose_name="질문", max_length=200, null=True)
    answer_type = models.IntegerField(choices=AT, null=False, verbose_name="답변 타입")


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField(verbose_name="답변", max_length=200, null=True)
    answer_count = models.IntegerField(verbose_name="질문순서")


class Process(models.Model):
    AR_STATE = [
        (0, "deleted"),
        (1, "in_progress"),
        (2, "completed"),
        (3, "cancelled"),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="processes")
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="processes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="processes")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="processes")
    
    created_at = models.DateTimeField('created_at', auto_now=True)
    state = models.IntegerField(choices=AR_STATE, default=1)
    marketing = models.IntegerField(choices=AR_STATE, default=1)
    

class  ProcessUser(models.Model):
    
    id = models.AutoField(primary_key=True)
    prcess = models.ForeignKey(Process, on_delete=models.CASCADE, related_name="processes")
    name = models.CharField(verbose_name="이름", max_length=20, null=True)
    tel = models.CharField(verbose_name="연락처", max_length=20, null=True)
