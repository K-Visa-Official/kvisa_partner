from rest_framework import serializers
from .models import Work, Question, Answer, Process
from user.serializers import UserSerializer
from .models import ProcessUser


class WorkSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Work
        fields = "__all__"

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

    class Meta:
        model = ProcessUser
        fields = ['id', 'name', 'tel', 'work', 'process' , 'state' , 'created_at']

    def get_work(self, obj):
        # ✅ obj.process를 통해 work에 접근
        if obj.process and obj.process.work:
            return WorkSerializer(obj.process.work).data
        return None  # work가 없을 경우 None 반환
    
    def get_process(self, obj):
        # ✅ obj.process를 직렬화해야 함
        return ProcessSerializer(obj.process).data if obj.process else None
