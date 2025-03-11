from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # 기본 페이지 크기 (10개)
    page_size_query_param = 'page_size'  # 쿼리 파라미터로 개수 조절 가능
    max_page_size = 100  # 최대 100개까지 요청 가능

class CustomPagination_five(PageNumberPagination):
    page_size = 5  # 기본 페이지 크기 (10개)
    page_size_query_param = 'page_size'  # 쿼리 파라미터로 개수 조절 가능
    max_page_size = 100  # 최대 100개까지 요청 가능
