import os
from openai import OpenAI
import requests
import json
from django.conf import settings


class OpenRouterService:
    """Сервис для работы с OpenRouter AI API"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'OPENROUTER_API_KEY', os.getenv('OPENROUTER_API_KEY'))
        self.base_url = "https://openrouter.ai/api/v1"
        self.site_url = getattr(settings, 'OPENROUTER_SITE_URL', os.getenv('OPENROUTER_SITE_URL', ''))
        self.site_name = getattr(settings, 'OPENROUTER_SITE_NAME', os.getenv('OPENROUTER_SITE_NAME', ''))
        
        if not self.api_key:
            raise ValueError("OpenRouter API key не найден. Установите OPENROUTER_API_KEY в настройках или переменных окружения.")
        
        # Инициализация клиента OpenAI с базовым URL OpenRouter
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
    
    def get_available_models(self):
        """Получить список доступных моделей"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Ошибка при получении моделей: {str(e)}"}
    
    def chat_completion(self, messages, model="openai/gpt-3.5-turbo", **kwargs):
        """
        Отправить запрос на завершение чата
        
        Args:
            messages: список сообщений для чата
            model: название модели (по умолчанию gpt-3.5-turbo)
            **kwargs: дополнительные параметры для API
        """
        try:
            extra_headers = {}
            if self.site_url:
                extra_headers["HTTP-Referer"] = self.site_url
            if self.site_name:
                extra_headers["X-Title"] = self.site_name
            
            completion = self.client.chat.completions.create(
                extra_headers=extra_headers,
                model=model,
                messages=messages,
                **kwargs
            )
            
            return {
                "success": True,
                "response": completion.choices[0].message.content,
                "model": completion.model,
                "usage": completion.usage._asdict() if completion.usage else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def simple_chat(self, prompt, model="openai/gpt-3.5-turbo", system_message=None):
        """
        Простой чат с одним сообщением
        
        Args:
            prompt: пользовательский запрос
            model: модель для использования
            system_message: системное сообщение (опционально)
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        return self.chat_completion(messages, model)
    
    def stream_chat(self, messages, model="openai/gpt-3.5-turbo", **kwargs):
        """
        Стриминговый чат
        
        Args:
            messages: список сообщений для чата
            model: название модели
            **kwargs: дополнительные параметры
        """
        try:
            extra_headers = {}
            if self.site_url:
                extra_headers["HTTP-Referer"] = self.site_url
            if self.site_name:
                extra_headers["X-Title"] = self.site_name
            
            stream = self.client.chat.completions.create(
                extra_headers=extra_headers,
                model=model,
                messages=messages,
                stream=True,
                **kwargs
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Ошибка: {str(e)}"


# Функция-помощник для быстрого доступа
def get_openrouter_service():
    """Получить экземпляр сервиса OpenRouter"""
    return OpenRouterService()