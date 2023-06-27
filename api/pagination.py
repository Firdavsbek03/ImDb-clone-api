from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination


class MoviesPageNumberPagination(PageNumberPagination):
    page_size=3
    page_query_param = 'page_number'
    page_size_query_param = 'size'
    max_page_size = 7
    last_page_strings = ['end']


class MoviesLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 4
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'


class MoviesCursorPagination(CursorPagination):
    page_size = 2
    cursor_query_param = 'pointer'
    ordering = 'created'

