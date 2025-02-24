from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkSerializer, QuestionSerializer, AnswerSerializer ,ProcessSerializer , ProcessUserSerializer
from .models import Work, Question, Answer , Process , ProcessUser
from config.permissions import IsStaff
from user.models import User
from user.serializers import UserSerializer

from config.paging import CustomPagination

from django.db.models import Q

########################### 어드민 ###########################
# 질문 등록
@api_view(['POST'])
@permission_classes([IsStaff])
def postwork(request):

    data = request.data
    
    # 'user' 필드를 요청 데이터에 추가
     # 'user' 필드를 현재 인증된 사용자 ID로 설정
    user_id = data.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    data['user'] = user_id  # user를 직접 추가하여 serializer에 전달
    data.pop("user_id", None) 
    
    # Work 데이터 저장
    work_serializer = WorkSerializer(data=data)
    if not work_serializer.is_valid():
        return Response(work_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    work_instance = work_serializer.save()  # Work 객체 저장

    if data.get("language") == 0 :
        user.work_count += 1 
        user.save()
    else :
        user.work_count_ch += 1 
        user.save()

    if not work_serializer.is_valid():
        return Response(work_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    work_instance = work_serializer.save()  # Work 객체 저장
    work_id = work_instance.id  # 저장된 객체의 ID 가져오기

    questions_data = data.get("questions", [])

    for question_data in questions_data:
        question_text = question_data.get("question")
        answer_type = question_data.get("answer_type")

        if not question_text:
            continue  # 질문 텍스트가 없으면 건너뛰기

        # 질문 저장
        question = Question.objects.create(
            work=work_instance,
            question=question_text,
            answer_type=answer_type,
        )

        answers_data = question_data.get("answers", [])

        for answer_data in answers_data:
            answer_text = answer_data.get("answer")
            answer_count = answer_data.get("sort")

            if not answer_text:
                continue  # 답변 텍스트가 없으면 건너뛰기

            # 답변 저장
            Answer.objects.create(
                question=question,  # 수정된 부분: question 객체를 할당
                answer=answer_text,  # 답변 텍스트
                answer_count=answer_count,  # 질문 순서
            )

    return Response(work_serializer.data, status=status.HTTP_201_CREATED)

# 이미지 등록
@api_view(['PATCH'])
@permission_classes([IsStaff])
def change_image(request):
    work_instance = Work.objects.get(id=request.data['id'])
    work_instance.detail = request.data["detail_url"]
    work_instance.detail_second = request.data["detail_second"]
    work_instance.save()
    serializer = WorkSerializer(work_instance)
    return Response(serializer.data, status=status.HTTP_200_OK)                    

# 질문조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_work(request, work_id):
    try:
        work = Work.objects.get(id=work_id)
        serializer = WorkSerializer(work)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Work.DoesNotExist:
        return Response({'detail': 'Work not found'}, status=status.HTTP_404_NOT_FOUND)

# 업무 이름 및 정보 수정
@api_view(['PUT'])
@permission_classes([IsStaff])
def update_work(request, work_id):
    try:
        work = Work.objects.get(id=work_id)
        work_serializer = WorkSerializer(work, data=request.data)

        if work_serializer.is_valid():
            work_serializer.save()
            return Response(work_serializer.data, status=status.HTTP_200_OK)
        return Response(work_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Work.DoesNotExist:
        return Response({'detail': 'Work not found'}, status=status.HTTP_404_NOT_FOUND)
    
# 질문수정    
@api_view(['PUT'])
@permission_classes([IsStaff])
def update_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question_serializer = QuestionSerializer(question, data=request.data)

        if question_serializer.is_valid():
            question_serializer.save()
            return Response(question_serializer.data, status=status.HTTP_200_OK)
        return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Question.DoesNotExist:
        return Response({'detail': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
    
# 답변수정    
@api_view(['PUT'])
@permission_classes([IsStaff])
def update_answer(request, answer_id):
    try:
        answer = Answer.objects.get(id=answer_id)
        answer_serializer = AnswerSerializer(answer, data=request.data)

        if answer_serializer.is_valid():
            answer_serializer.save()
            return Response(answer_serializer.data, status=status.HTTP_200_OK)
        return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Answer.DoesNotExist:
        return Response({'detail': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)

# 업무 삭제
@api_view(['DELETE'])
@permission_classes([IsStaff])
def delete_work(request, work_id):
    try:
        work = Work.objects.get(id=work_id)
        work.delete()
        return Response({'detail': 'Work deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Work.DoesNotExist:
        return Response({'detail': 'Work not found'}, status=status.HTTP_404_NOT_FOUND)

# 질문 삭제
@api_view(['DELETE'])
@permission_classes([IsStaff])
def delete_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.delete()
        return Response({'detail': 'Question deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Question.DoesNotExist:
        return Response({'detail': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

# 답변 삭제
@api_view(['DELETE'])
@permission_classes([IsStaff])
def delete_answer(request, answer_id):
    try:
        answer = Answer.objects.get(id=answer_id)
        answer.delete()
        return Response({'detail': 'Answer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Answer.DoesNotExist:
        return Response({'detail': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)

########################### 의뢰인 ###########################
# 업체 등록한 업무리스트
@api_view(['GET'])
@permission_classes([AllowAny])
def get_work_bu(request, pk):
    # 쿼리 파라미터에서 'language' 값 받기
    la = request.GET.get('language')

    # 업체가 등록한 업무 필터링 (언어 필터링이 있을 경우)
    if la:
        work = Work.objects.filter(user=pk, language=la).order_by('-order')
    else:
        # 언어 필터링 없이 전체 데이터 반환
        work = Work.objects.filter(user=pk).order_by('-order')
    
    if not work.exists():
        user = User.objects.filter(id=pk)
        # User에 대한 직렬화 진행 (적절한 UserSerializer 사용)
        user_serializer = UserSerializer(user, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    # 직렬화된 데이터 반환
    serializer = WorkSerializer(work, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# 업체 등록한 업무상세보기
@api_view(['GET'])
@permission_classes([AllowAny])
def get_work_detail(request, pk):
    # 쿼리 파라미터에서 'language' 값 받기
    work = Work.objects.filter(id=pk)
      
    # 업체가 등록한 업무 필터링 (언어 필터링이 있을 경우)  
    # 직렬화된 데이터 반환
    serializer = WorkSerializer(work, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# 질문 답변 리스트
@api_view(['GET'])
@permission_classes([AllowAny])
def get_work_qu_an(request, pk):

    # 업체가 등록한 업무 필터링 (언어 필터링이 있을 경우)
    questions = Question.objects.filter(work_id=pk).prefetch_related('answers')  # 🔹 Answer까지 한 번에 불러오기
    
    # 🔹 직렬화 (Question + 연결된 Answer 포함)
    serializer = QuestionSerializer(questions, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# 업무 진행
@api_view(['POST'])
@permission_classes([AllowAny])
def post_work(request):
    user = request.data.get("user")  # 현재 로그인한 사용자
    work_id = request.data.get("work")  # 업무 ID
    # name = request.data.get("name")  # 사용자 이름
    # tel = request.data.get("tel")  # 연락처
    # marketing = request.data.get("marketing")  
    question = request.data.get("questions")  # 연락처
    answer = request.data.get("answers")  

    if not work_id:
        return Response({"detail": "Work ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        work = Work.objects.get(id=work_id)
    except Work.DoesNotExist:
        return Response({"detail": "Work not found"}, status=status.HTTP_404_NOT_FOUND)

   
    # Process 생성
    process = Process.objects.create(
        user=user,
        work=work,
        question = question,
        answer = answer,
    )

    # ProcessUser 생성
    # process_user = ProcessUser.objects.create(
    #     process=process,
    #     name=name,
    #     tel=tel,
    #     state=1,  # 진행 중 (in_progress)
    #     marketing = marketing
    # )

    return Response({
        "detail": "Process created successfully" ,
        "return": process.id ,
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def post_work_user(request):
    user_id = request.data.get("id")  # 현재 로그인한 사용자
    name = request.data.get("name")  # 사용자 이름
    tel = request.data.get("tel")  # 연락처
    marketing = request.data.get("marketing")  # 마케팅 동의 여부
    lang = request.data.get("lang")  # 마케팅 동의 여부

    try:
        # process_id에 해당하는 Process 객체 가져오기
        process = Process.objects.get(id=user_id)  # process_id는 user_id를 통해 가져오는 방식으로 변경
    except Process.DoesNotExist:
        return Response({"detail": "Process not found"}, status=status.HTTP_404_NOT_FOUND)

    # ProcessUser 생성
    process_user = ProcessUser.objects.create(
        process=process,  # 유효한 Process 객체를 연결
        name=name,
        tel=tel,
        state=0,  # 진행 중 (in_progress)
        marketing=marketing,
        lang = lang
    )

    return Response({
        "detail": "ProcessUser created successfully",
        "return": process_user.id,
    }, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def pro_name_change(request):
    try:
        progress_instance = ProcessUser.objects.get(id=request.data['id'])
        progress_instance.name = request.data["name"]
        progress_instance.tel = request.data["tel"]
        progress_instance.save()
        serializer = ProcessUserSerializer(progress_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ProcessUser.DoesNotExist:
        return Response({"error": "ProcessUser not found"}, status=status.HTTP_404_NOT_FOUND)       


# 진행중인 업무 조회
@api_view(['GET'])
@permission_classes([AllowAny])
def get_work_check(request):

    tel = request.GET.get("tel")

    process = ProcessUser.objects.filter(tel = tel).order_by("-id")

    serializer = ProcessUserSerializer(process, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)



# 진행중인 업무 확인
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_work(request,id):

    state = request.data.get("state")
    name = request.data.get("name")
    created_at = request.data.get("created_at")
    
    filters = Q(user=request.user)  # 현재 사용자 필터

    if state:
        filters &= Q(state=state)
    
    if created_at:
        filters &= Q(created_at__date=created_at)  # 날짜 필터
    
    if name:
        filters &= Q(work__choice__icontains=name)  # 업무 이름 필터

    process = Process.objects.filter(filters).order_by("-created_at")

    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(process, request)
    serializer = ProcessSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)




# 진행상태 변경
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_state(request,id) :
    state = request.data.get("state")
    pk  = request.data.get("id")

    process = Process.objects.filter(id = pk)

    process.state = state
    process.save()

    serializer = ProcessSerializer(process, many=False)
    data = serializer.data

    return Response(data, status=status.HTTP_200_OK)