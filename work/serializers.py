from rest_framework import serializers
from .models import Work, Question, Answer, Process
from user.serializers import UserSerializer

class WorkSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Work
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"


class ProcessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"