from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    """Отображает главную страницу сайта.

    Рендерит шаблон главной страницы и возвращает его в виде HTTP-ответа.

    Args:
        request (HttpRequest): Объект HTTP-запроса от пользователя.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон homepage.html.
    """
    return render(request, 'homepage.html')


def about(request):
    """Отображает страницу «О проекте».

    Рендерит шаблон страницы с информацией о проекте или компании
    и возвращает его в виде HTTP-ответа.

    Args:
        request (HttpRequest): Объект HTTP-запроса от пользователя.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон about.html.
    """
    return render(request, 'about.html')
