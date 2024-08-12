from django.test import TestCase
from bs4 import BeautifulSoup
import re


class ProxyTestCase(TestCase):
    def test_proxy(self):
        """
        Проверка функциональности проксирования запросов к стороннему ресурсу
        и модификации содержимого ответа
        """
        response = self.client.get('http://127.0.0.1:8232/item?id=13713480')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        for text_element in soup.find_all(text=True):
            if text_element.parent.name not in ['script', 'style']:
                pattern = r'\b\w{6}\b'
                match = re.search(pattern, text_element)
                if match:
                    end = match.end()
                    # Проверяем, есть ли следующие два символа после совпадения и если есть, то равны '™'
                    if end + 2 >= len(text_element):
                        self.assertEqual(text_element[end:end+1], '™')

