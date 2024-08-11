from django.http import HttpResponse
from django.views import View
import requests
from bs4 import BeautifulSoup
import re


class ProxyView(View):
    """
    ProxyView предоставляет функциональность проксирования запросов к стороннему ресурсу
    и модификации содержимого ответа.

    Этот класс отвечает за следующие задачи:
    - Принимает HTTP-запрос от клиента и перенаправляет его на целевой сайт (например, Hacker News).
    - Получает ответ от целевого сайта, включая HTML-содержимое.
    - Обрабатывает полученный HTML-контент, добавляя символ "™" после каждого шестибуквенного слова.
    - Возвращает измененный HTML-контент клиенту с сохранением всех функциональных возможностей страницы.

    Основные методы:
    - `get(self, request, *args, **kwargs)`: Обрабатывает GET-запросы. Получает контент с целевого сайта,
      модифицирует его и возвращает клиенту.
    - `modify_content(self, content)`: Изменяет HTML-контент, добавляя "™" к шестибуквенным словам.
    """
    def modify_content(self, content):
        # Добавляем ™ после каждого шестибуквенного слова
        def add_tm(match):
            # match.group(0) возвращает строку, которая соответствует найденному совпадению по регулярному выражению
            return match.group(0) + '™'

        # Изменяем текст внутри HTML-контента
        # заменяет все найденные в строке content совпадения с регулярным выражением
        modified_content = re.sub(r'\b\w{6}\b', add_tm, content)
        return modified_content

    def get(self, request, path=''):
        # Создаем URL для запроса к Hacker News
        target_url = f"https://news.ycombinator.com/{path}"
        query_string = request.META['QUERY_STRING']
        if query_string:
            target_url += '?' + query_string

        # Отправляем запрос к Hacker News
        response = requests.get(target_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Модифицируем текстовый контент страницы
        for text_element in soup.find_all(text=True):
            if text_element.parent.name not in ['script', 'style']:
                new_text = self.modify_content(text_element)
                # заменяет существующий текст в HTML-документе на модифицированный текст
                text_element.replace_with(new_text)

        # Возвращаем модифицированный контент клиенту
        return HttpResponse(str(soup), content_type=response.headers['Content-Type'])
