from django.urls import path
from . import views

urlpatterns = [
    ########################### 어드민 ###########################
    path('admin/work/', views.postwork, name='post_work'),  # 질문 등록

    path('admin/work/change', views.change_image, name='post_work'),  # 이미지 등록

    path('admin/work/change/no', views.change_image_work_change, name='post_work'),  # 이미지 등록

    path('admin/work/order', views.order_change, name='order_change'),  # 업무 순서변경
    
    path('admin/work/<int:work_id>/', views.get_work, name='get_work'),  # 질문조회

    path('admin/visa/', views.visa_intro, name='get_work'),  # 접수된 업무 리스트
    
    ########################### 의뢰인 ###########################
    path('client/works/<str:pk>', views.get_work_bu, name='get_work_list'),  # 업체가 등록한 업무 리스트

    path('client/work/detail/<str:pk>', views.get_work_detail, name='get_work_list'),  # 업체가 등록한 업무 리스트
    path('client/progress/edit', views.pro_name_change, name='edit'),  # 업체가 등록한 업무 리스트

    path('client/works/detail/<str:pk>', views.get_work_qu_an, name='get_work_list'),  # 업체가 등록한 업무 리스트
    path('client/crm', views.get_work_check, name='get_work_list'),  # 업체가 등록한 업무 리스트

    path('client/work/', views.post_work, name='post_work'),  # 업무 등록
    path('client/work/user', views.post_work_user, name='post_work'),  # 업무 등록

    path('client/works/in_progress/', views.get_work, name='get_in_progress_work'),  # 진행중인 업무 확인
    path('client/work/state/<int:id>/', views.change_state, name='change_work_state'),  # 진행상태 변경
]
