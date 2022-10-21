from django.core.paginator import Paginator
from django.http import HttpRequest

LIMIT_POSTS = 10


def paginate(queryset: None, request: HttpRequest) -> tuple:
    """
    Функция постраничного разделения в зависимости
    от объемов входящей информации,
    вынесена в отдельную область.
    """
    paginator = Paginator(queryset, LIMIT_POSTS)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return page_object