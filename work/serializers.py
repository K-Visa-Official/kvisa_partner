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

    class Meta:
        model = ProcessUser
        fields = ['id', 'name', 'tel', 'work']

    def get_work(self, obj):
        # ProcessUser에서 연결된 Process를 통해 Work를 가져오기
        return WorkSerializer(obj.process.work).data