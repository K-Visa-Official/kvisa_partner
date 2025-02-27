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
from django.http import JsonResponse
import json

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
            answer_count = answer_data.get("answer_count")

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

@api_view(['PATCH'])
@permission_classes([IsStaff])
def change_image_work_change(request):
    try:
        # 기존 작업 데이터 가져오기
        work_before = Work.objects.get(id=request.data['before_id'])
        
        # 새로운 작업 데이터 가져오기
        work_new = Work.objects.get(id=request.data['new_id'])

        # 새로운 작업 객체 수정
        if 'detail_url' in request.data and request.data['detail_url']:
            work_new.detail = request.data["detail_url"]
        else :
            work_new.detail = work_before.detail

        if 'detail_second' in request.data and request.data['detail_second']:
            work_new.detail_second = request.data["detail_second"]
        else :
            work_new.detail_second = work_before.detail_second

        if work_new.language == 0 :
            user = User.objects.get(id=work_new.user)
            user.work_count  -= 1 
            user.save()
        elif work_new.language == 1 :
            user = User.objects.get(id=work_new.user)
            user.work_count_ch  -= 1 
            user.save()

        work_new.save()


        # 기존 작업 삭제 (필요한 경우(())
        work_before.delete()

        # 변경된 작업 객체 반환
        serializer = WorkSerializer(work_new)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Work.DoesNotExist:
        return Response({'detail': 'Work not found'}, status=status.HTTP_404_NOT_FOUND)
    
# 업무 순서 변경
@api_view(['PATCH'])
@permission_classes([IsStaff])
def order_change(request):
    try:
        user_id = request.data.get("pk")
        work_id = request.data.get("work_id")
        direction = request.data.get("direction")

        work = Work.objects.get(id=work_id, user=user_id)
            
        if direction == "up":
            # 현재 order보다 작은 값 중 가장 큰 값을 가진 work 찾기
            prev_work = Work.objects.filter(user=user_id, order__lt=work.order).order_by("-order").first()
            if prev_work:
                work.order, prev_work.order = prev_work.order, work.order
                work.save()
                prev_work.save()

            return JsonResponse({"status": "success", "message": "Order updated"})
        
        elif direction == "down":
            # 현재 order보다 큰 값 중 가장 작은 값을 가진 work 찾기
            next_work = Work.objects.filter(user=user_id, order__gt=work.order).order_by("order").first()
            if next_work:
                work.order, next_work.order = next_work.order, work.order
                work.save()
                next_work.save()

            return JsonResponse({"status": "success", "message": "Order updated"})
        
    except Work.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Work not found"}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

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

# 접수된 업무 현황
@api_view(['GET'])
@permission_classes([IsStaff])
def visa_intro(request) :
    paginator = CustomPagination()

    filters = Q()
    
    # 비즈니스 필터 추가
    business = request.GET.get("business")
    if business:
        filters &= Q(business=business)

    # 생성 날짜 필터 추가
    create_at = request.GET.get("created_at")
    if create_at:
        filters &= Q(created_at=create_at)


    # 데이터 필터링 및 페이징 처리
    queryset = ProcessUser.objects.filter(filters).order_by('-created_at')
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = ProcessUserSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


########################### 의뢰인 ###########################
# 업체 등록한 업무리스트
@api_view(['GET'])
@permission_classes([AllowAny])
def get_work_bu(request, pk):
    # 쿼리 파라미터에서 'language' 값 받기
    la = request.GET.get('language')

    # 업체가 등록한 업무 필터링 (언어 필터링이 있을 경우)
    if la:
        work = Work.objects.filter(user=pk, language=la).order_by('order')
    else:
        # 언어 필터링 없이 전체 데이터 반환
        work = Work.objects.filter(user=pk).order_by('order')
    
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

    name = request.GET.get("name")
    if tel :
        process = ProcessUser.objects.filter(tel = tel).order_by("-id")
    else :
        process = ProcessUser.objects.filter(name = name).order_by("-id")
        

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