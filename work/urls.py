from django.urls import path
from . import views

urlpatterns = [
    ########################### 어드민 ###########################
    path('admin/work/', views.postwork, name='post_work'),  # 질문 등록

    path('admin/work/change', views.change_image, name='post_work'),  # 이미지 등록
    path('admin/work/<int:work_id>/', views.get_work, name='get_work'),  # 질문조회
    path('admin/work/update/<int:work_id>/', views.update_work, name='update_work'),  # 업무 이름 및 정보 수정
    path('admin/question/update/<int:question_id>/', views.update_question, name='update_question'),  # 질문 수정
    path('admin/answer/update/<int:answer_id>/', views.update_answer, name='update_answer'),  # 답변 수정
    path('admin/work/delete/<int:work_id>/', views.delete_work, name='delete_work'),  # 업무 삭제
    path('admin/question/delete/<int:question_id>/', views.delete_question, name='delete_question'),  # 질문 삭제
    path('admin/answer/delete/<int:answer_id>/', views.delete_answer, name='delete_answer'),  # 답변 삭제

    ########################### 의뢰인 ###########################
    path('client/works/<str:pk>', views.get_work_bu, name='get_work_list'),  # 업체가 등록한 업무 리스트
    path('client/work/', views.post_work, name='post_work'),  # 업무 등록
    path('client/works/in_progress/', views.get_work, name='get_in_progress_work'),  # 진행중인 업무 확인
    path('client/work/state/<int:id>/', views.change_state, name='change_work_state'),  # 진행상태 변경
]
