from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def page_not_found(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')


def server_error(request):
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'core/403.html', status=403)


COUNT_ROWS = 10


def make_pntr(queryset, request):
    paginator = Paginator(queryset, COUNT_ROWS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
    }


@login_required
def index(request):
    """Главная страница"""
    template = 'core/index.html'
    title = 'Network MGMT main page'
    context = {
        'title': title
    }
    return render(request, template, context)
