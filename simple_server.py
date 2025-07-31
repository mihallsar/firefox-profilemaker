#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой веб-сервер для демонстрации Firefox Profile Maker
Этот сервер показывает основную функциональность программы без сложной настройки Django
"""

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import parse_qs
import json

class ProfileMakerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_main_page().encode('utf-8'))
        elif self.path == '/about':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_about_page().encode('utf-8'))
        elif self.path == '/download':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_download_page().encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/create':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_result_page(form_data).encode('utf-8'))
    
    def get_main_page(self):
        return """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firefox Profile Maker - Создатель безопасных профилей</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #FF6600; text-align: center; }
        h2 { color: #333; border-bottom: 2px solid #FF6600; padding-bottom: 10px; }
        .addon { 
            background: #f0f8ff; 
            padding: 15px; 
            margin: 10px 0; 
            border-left: 4px solid #FF6600;
            border-radius: 5px;
        }
        .addon h3 { margin-top: 0; color: #FF6600; }
        button { 
            background: #FF6600; 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 5px; 
            font-size: 16px;
            cursor: pointer;
            margin: 10px 5px;
        }
        button:hover { background: #E55500; }
        .warning { 
            background: #fff3cd; 
            border: 1px solid #ffeaa7; 
            padding: 15px; 
            border-radius: 5px;
            margin: 20px 0;
        }
        .nav { text-align: center; margin: 20px 0; }
        .nav a { 
            color: #FF6600; 
            text-decoration: none; 
            margin: 0 15px;
            font-weight: bold;
        }
        .profile-type {
            border: 2px solid #ddd;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            cursor: pointer;
        }
        .profile-type:hover { border-color: #FF6600; }
        .profile-type input[type="radio"] { margin-right: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦊 Firefox Profile Maker</h1>
        <p style="text-align: center; font-size: 18px; color: #666;">
            Создавай безопасные профили Firefox одним кликом!
        </p>
        
        <div class="nav">
            <a href="/">Главная</a>
            <a href="/about">О программе</a>
            <a href="/download">Скачать расширения</a>
        </div>

        <div class="warning">
            <strong>⚠️ Внимание!</strong> Это демонстрационная версия программы. 
            Для получения реального профиля используйте ручную установку расширений 
            (см. файл ИНСТРУКЦИЯ_ПО_ИСПОЛЬЗОВАНИЮ.md)
        </div>

        <h2>🛡️ Выберите тип защиты</h2>
        
        <form method="post" action="/create">
            <div class="profile-type">
                <label>
                    <input type="radio" name="profile_type" value="basic" checked>
                    <strong>🟢 Базовая защита</strong>
                    <p>Блокировка рекламы и основных трекеров. Подходит для ежедневного использования.</p>
                </label>
            </div>
            
            <div class="profile-type">
                <label>
                    <input type="radio" name="profile_type" value="advanced">
                    <strong>🟡 Продвинутая защита</strong>
                    <p>Дополнительная защита от отпечатков браузера и продвинутого отслеживания.</p>
                </label>
            </div>
            
            <div class="profile-type">
                <label>
                    <input type="radio" name="profile_type" value="paranoid">
                    <strong>🔴 Максимальная защита</strong>
                    <p>Максимальная приватность. Некоторые сайты могут работать некорректно.</p>
                </label>
            </div>

            <h2>🔧 Дополнительные настройки</h2>
            
            <label>
                <input type="checkbox" name="addons" value="ublock" checked>
                <strong>uBlock Origin</strong> - блокировка рекламы и трекеров
            </label><br><br>
            
            <label>
                <input type="checkbox" name="addons" value="privacy_badger" checked>
                <strong>Privacy Badger</strong> - защита от невидимого отслеживания
            </label><br><br>
            
            <label>
                <input type="checkbox" name="addons" value="https_everywhere" checked>
                <strong>HTTPS Everywhere</strong> - принудительное использование HTTPS
            </label><br><br>
            
            <label>
                <input type="checkbox" name="addons" value="canvas_blocker">
                <strong>CanvasBlocker</strong> - защита от снятия отпечатков через Canvas
            </label><br><br>
            
            <label>
                <input type="checkbox" name="addons" value="clearurls">
                <strong>ClearURLs</strong> - очистка URL от трекинговых параметров
            </label><br><br>

            <div style="text-align: center; margin: 30px 0;">
                <button type="submit">🚀 Создать профиль</button>
            </div>
        </form>

        <h2>📚 Что дальше?</h2>
        <ol>
            <li><strong>Создайте профиль</strong> с помощью формы выше</li>
            <li><strong>Скачайте</strong> сгенерированный файл профиля</li>
            <li><strong>Установите</strong> профиль в Firefox</li>
            <li><strong>Наслаждайтесь</strong> безопасным браузингом!</li>
        </ol>
    </div>
</body>
</html>
        """

    def get_about_page(self):
        return """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>О программе - Firefox Profile Maker</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #FF6600; text-align: center; }
        h2 { color: #333; border-bottom: 2px solid #FF6600; padding-bottom: 10px; }
        .nav { text-align: center; margin: 20px 0; }
        .nav a { 
            color: #FF6600; 
            text-decoration: none; 
            margin: 0 15px;
            font-weight: bold;
        }
        .feature {
            background: #f8f9fa;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            border-left: 4px solid #FF6600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦊 О программе Firefox Profile Maker</h1>
        
        <div class="nav">
            <a href="/">Главная</a>
            <a href="/about">О программе</a>
            <a href="/download">Скачать расширения</a>
        </div>

        <h2>📖 Что это?</h2>
        <p>
            Firefox Profile Maker - это инструмент для автоматического создания 
            безопасных профилей браузера Firefox с предустановленными расширениями 
            для защиты приватности.
        </p>

        <h2>🎯 Цель проекта</h2>
        <p>
            Упростить процесс настройки безопасного браузера для пользователей, 
            которые хотят защитить свою приватность в интернете, но не знают, 
            как это сделать правильно.
        </p>

        <h2>✨ Возможности</h2>
        
        <div class="feature">
            <h3>🛡️ Автоматическая настройка</h3>
            <p>Программа автоматически настраивает Firefox с оптимальными настройками безопасности.</p>
        </div>
        
        <div class="feature">
            <h3>🔧 Гибкие профили</h3>
            <p>Выбирайте между базовой, продвинутой и максимальной защитой в зависимости от ваших потребностей.</p>
        </div>
        
        <div class="feature">
            <h3>📦 Готовые расширения</h3>
            <p>Включает проверенные расширения для блокировки рекламы, защиты от трекинга и повышения безопасности.</p>
        </div>
        
        <div class="feature">
            <h3>🚀 Простота использования</h3>
            <p>Создание безопасного профиля занимает всего несколько кликов.</p>
        </div>

        <h2>🔒 Включенные расширения</h2>
        <ul>
            <li><strong>uBlock Origin</strong> - мощный блокировщик рекламы и трекеров</li>
            <li><strong>Privacy Badger</strong> - защита от невидимого отслеживания</li>
            <li><strong>HTTPS Everywhere</strong> - принудительное использование безопасных соединений</li>
            <li><strong>CanvasBlocker</strong> - защита от снятия цифровых отпечатков</li>
            <li><strong>ClearURLs</strong> - удаление трекинговых параметров из ссылок</li>
            <li><strong>Cookie AutoDelete</strong> - автоматическое удаление cookies</li>
            <li><strong>Decentraleyes</strong> - защита от CDN-отслеживания</li>
            <li><strong>Temporary Containers</strong> - изоляция вкладок</li>
            <li><strong>Multi-Account Containers</strong> - разделение контекстов</li>
        </ul>

        <h2>💡 Для кого этот инструмент?</h2>
        <ul>
            <li>🆕 <strong>Новичков</strong>, которые хотят защитить свою приватность</li>
            <li>👨‍💻 <strong>Разработчиков</strong>, которым нужны готовые профили для тестирования</li>
            <li>🛡️ <strong>Энтузиастов приватности</strong>, ценящих автоматизацию</li>
            <li>🏢 <strong>Организаций</strong>, внедряющих безопасные браузеры</li>
        </ul>

        <h2>⚖️ Лицензия</h2>
        <p>
            Проект распространяется под свободной лицензией и имеет открытый исходный код. 
            Вы можете использовать, изменять и распространять программу свободно.
        </p>
    </div>
</body>
</html>
        """

    def get_download_page(self):
        return """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Скачать расширения - Firefox Profile Maker</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #FF6600; text-align: center; }
        h2 { color: #333; border-bottom: 2px solid #FF6600; padding-bottom: 10px; }
        .nav { text-align: center; margin: 20px 0; }
        .nav a { 
            color: #FF6600; 
            text-decoration: none; 
            margin: 0 15px;
            font-weight: bold;
        }
        .addon-link {
            display: block;
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            text-decoration: none;
            color: #333;
            border-radius: 5px;
            border-left: 4px solid #FF6600;
            transition: background-color 0.3s;
        }
        .addon-link:hover {
            background: #e9ecef;
        }
        .addon-name {
            font-weight: bold;
            color: #FF6600;
            font-size: 18px;
        }
        .addon-description {
            margin-top: 5px;
            color: #666;
        }
        .instruction {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦊 Скачать расширения Firefox</h1>
        
        <div class="nav">
            <a href="/">Главная</a>
            <a href="/about">О программе</a>
            <a href="/download">Скачать расширения</a>
        </div>

        <div class="instruction">
            <h3>📝 Как установить расширение:</h3>
            <ol>
                <li>Кликните по ссылке на расширение ниже</li>
                <li>На странице Mozilla Addons нажмите синюю кнопку "Добавить в Firefox"</li>
                <li>Подтвердите установку в появившемся окне</li>
                <li>Повторите для всех нужных расширений</li>
            </ol>
        </div>

        <h2>🛡️ Рекомендуемые расширения</h2>

        <a href="https://addons.mozilla.org/firefox/addon/ublock-origin/" class="addon-link" target="_blank">
            <div class="addon-name">uBlock Origin</div>
            <div class="addon-description">
                Эффективный блокировщик рекламы и трекеров. Экономит трафик и ускоряет загрузку страниц.
            </div>
        </a>

        <a href="https://addons.mozilla.org/firefox/addon/privacy-badger17/" class="addon-link" target="_blank">
            <div class="addon-name">Privacy Badger</div>
            <div class="addon-description">
                Автоматически блокирует шпионские трекеры, которые следят за вами в интернете.
            </div>
        </a>

        <a href="https://addons.mozilla.org/firefox/addon/https-everywhere/" class="addon-link" target="_blank">
            <div class="addon-name">HTTPS Everywhere</div>
            <div class="addon-description">
                Автоматически переключает сайты на безопасное HTTPS-соединение, когда это возможно.
            </div>
        </a>

        <a href="https://addons.mozilla.org/firefox/addon/canvasblocker/" class="addon-link" target="_blank">
            <div class="addon-name">CanvasBlocker</div>
            <div class="addon-description">
                Защищает от снятия цифровых отпечатков через Canvas API и другие методы.
            </div>
        </a>

        <a href="https://addons.mozilla.org/firefox/addon/clearurls/" class="addon-link" target="_blank">
            <div class="addon-name">ClearURLs</div>
            <div class="addon-description">
                Автоматически удаляет трекинговые параметры из URL-адресов.
            </div>
        </a>

        <h2>🔧 Дополнительные расширения</h2>

        <a href="https://addons.mozilla.org/firefox/addon/cookie-autodelete/" class="addon-link" target="_blank">
            <div class="addon-name">Cookie AutoDelete</div>
            <div class="addon-description">
                Автоматически удаляет cookies и данные сайтов после закрытия вкладки.
            </div>
        </a>

        <a href="https://addons.mozilla.org/firefox/addon/decentraleyes/" class="addon-link" target="_blank">
            <div class="addon-name">Decentraleyes</div>
            <div class="addon-description">
                Защищает от отслеживания через CDN, предоставляя локальные копии библиотек.
            </div>
        </a>

        <a href="https://addons.mozilla.org/firefox/addon/temporary-containers/" class="addon-link" target="_blank">
            <div class="addon-name">Temporary Containers</div>
            <div class="addon-description">
                Автоматически открывает вкладки в изолированных контейнерах.
            </div>
        </a>

        <a href="https://addons.mozilla.org/firefox/addon/multi-account-containers/" class="addon-link" target="_blank">
            <div class="addon-name">Multi-Account Containers</div>
            <div class="addon-description">
                Позволяет разделять разные аккаунты и контексты в отдельных контейнерах.
            </div>
        </a>

        <div class="instruction">
            <h3>💡 Совет:</h3>
            <p>
                Для базовой защиты достаточно установить первые 3-4 расширения. 
                Остальные добавляйте по мере необходимости и понимания их функций.
            </p>
        </div>
    </div>
</body>
</html>
        """

    def get_result_page(self, form_data):
        profile_type = form_data.get('profile_type', ['basic'])[0]
        addons = form_data.get('addons', [])
        
        profile_names = {
            'basic': 'Базовая защита',
            'advanced': 'Продвинутая защита', 
            'paranoid': 'Максимальная защита'
        }
        
        addon_names = {
            'ublock': 'uBlock Origin',
            'privacy_badger': 'Privacy Badger',
            'https_everywhere': 'HTTPS Everywhere',
            'canvas_blocker': 'CanvasBlocker',
            'clearurls': 'ClearURLs'
        }
        
        return f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Профиль создан - Firefox Profile Maker</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #FF6600; text-align: center; }}
        h2 {{ color: #333; border-bottom: 2px solid #FF6600; padding-bottom: 10px; }}
        .success {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: center;
        }}
        .nav {{ text-align: center; margin: 20px 0; }}
        .nav a {{ 
            color: #FF6600; 
            text-decoration: none; 
            margin: 0 15px;
            font-weight: bold;
        }}
        button {{ 
            background: #FF6600; 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 5px; 
            font-size: 16px;
            cursor: pointer;
            margin: 10px 5px;
        }}
        button:hover {{ background: #E55500; }}
        .profile-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        .addon-list {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        .warning {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 Профиль успешно создан!</h1>
        
        <div class="nav">
            <a href="/">Главная</a>
            <a href="/about">О программе</a>
            <a href="/download">Скачать расширения</a>
        </div>

        <div class="success">
            <h2>✅ Ваш профиль готов!</h2>
            <p>Профиль Firefox с типом защиты "{profile_names.get(profile_type, profile_type)}" был успешно создан.</p>
        </div>

        <div class="warning">
            <strong>⚠️ Это демо-версия!</strong><br>
            Настоящий файл профиля не создается. Для получения реального профиля:
            <ol>
                <li>Перейдите на страницу <a href="/download">Скачать расширения</a></li>
                <li>Установите нужные расширения вручную</li>
                <li>Или изучите файл ИНСТРУКЦИЯ_ПО_ИСПОЛЬЗОВАНИЮ.md</li>
            </ol>
        </div>

        <div class="profile-info">
            <h3>📋 Конфигурация профиля:</h3>
            <p><strong>Тип защиты:</strong> {profile_names.get(profile_type, profile_type)}</p>
            
            <div class="addon-list">
                <h4>🔧 Выбранные расширения:</h4>
                <ul>
                    {''.join([f'<li>{addon_names.get(addon, addon)}</li>' for addon in addons]) if addons else '<li>Не выбраны</li>'}
                </ul>
            </div>
        </div>

        <h2>📥 Что дальше?</h2>
        <ol>
            <li><strong>Установите Firefox</strong>, если еще не установлен</li>
            <li><strong>Перейдите на страницу загрузки расширений</strong> и установите их вручную</li>
            <li><strong>Настройте Firefox</strong> согласно рекомендациям</li>
            <li><strong>Наслаждайтесь</strong> безопасным просмотром!</li>
        </ol>

        <div style="text-align: center; margin: 30px 0;">
            <button onclick="window.location.href='/download'">📦 Перейти к расширениям</button>
            <button onclick="window.location.href='/'">🏠 На главную</button>
        </div>

        <div class="profile-info">
            <h3>💡 Полезные советы:</h3>
            <ul>
                <li>После установки расширений перезагрузите Firefox</li>
                <li>Настройте каждое расширение согласно вашим потребностям</li>
                <li>Регулярно обновляйте расширения для лучшей защиты</li>
                <li>Изучите настройки приватности в самом Firefox</li>
            </ul>
        </div>
    </div>
</body>
</html>
        """

def start_server(port=8000):
    """Запускает веб-сервер на указанном порту"""
    try:
        with socketserver.TCPServer(("", port), ProfileMakerHandler) as httpd:
            print(f"""
🦊 Firefox Profile Maker - Демо сервер запущен!

📍 Адрес: http://localhost:{port}
🌐 Откройте этот адрес в браузере

❗ Это демонстрационная версия программы.
📖 Полная инструкция находится в файле: ИНСТРУКЦИЯ_ПО_ИСПОЛЬЗОВАНИЮ.md

⏹️  Для остановки сервера нажмите Ctrl+C
            """)
            
            # Попытка автоматически открыть браузер
            try:
                webbrowser.open(f'http://localhost:{port}')
                print("🚀 Браузер должен открыться автоматически...")
            except:
                print("ℹ️  Откройте браузер вручную и перейдите по адресу выше")
            
            print("=" * 50)
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен. Удачного использования!")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Порт {port} уже используется. Попробуйте другой порт:")
            print(f"   python3 simple_server.py {port + 1}")
        else:
            print(f"❌ Ошибка запуска сервера: {e}")

if __name__ == "__main__":
    import sys
    
    # Возможность указать порт как аргумент
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Неверный формат порта. Используется порт по умолчанию 8000")
    
    start_server(port)