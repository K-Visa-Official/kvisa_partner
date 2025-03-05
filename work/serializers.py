from rest_framework import serializers
from .models import Work, Question, Answer, Process
from user.serializers import UserSerializer
from .models import ProcessUser
from user.models import User
# from django.contrib.auth import get_user_model

# User = get_user_model()

class WorkSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    
    # user = UserSerializer()
    class Meta:
        model = Work
        fields = "__all__"

    def get_question(self, obj):
        # obj.question이 Work 모델에서 연관된 Question 객체일 경우 직렬화
        return QuestionSerializer(obj.questions.all(), many=True).data
    
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"




class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"


class ProcessUserSerializer(serializers.ModelSerializer):
    work = serializers.SerializerMethodField()
    process = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = ProcessUser
        fields = "__all__"

    
    def get_user(self, obj):
        """Process를 통해 user 정보 가져오기"""
        if obj.process and obj.process.user:
            try:
                user = User.objects.get(id=obj.process.user)  # ✅ 문자열 ID를 User 객체로 변환
                return UserSerializer(user).data
            except User.DoesNotExist:
                return None
        return None
    
    def get_work(self, obj):
        # ✅ obj.process를 통해 work에 접근
        if obj.process and obj.process.work:
            return WorkSerializer(obj.process.work).data
        return None  # work가 없을 경우 None 반환
    
    def get_process(self, obj):
        # ✅ obj.process를 직렬화해야 함
        return ProcessSerializer(obj.process).data if obj.process else None
