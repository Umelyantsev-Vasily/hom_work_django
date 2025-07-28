# 🏷️ Django Catalog

🛒 **Каталог товаров** с главной страницей и контактами на Django + Bootstrap

![Django](https://img.shields.io/badge/Django-4.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-blue)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)

## 🚀 Запуск проекта

```
# 1. Клонировать репозиторий
git clone https://github.com/ваш-репозиторий/django-catalog.git

# 2. Перейти в папку проекта
cd django-catalog

# 3. Активировать виртуальное окружение (Linux/macOS)
source venv/bin/activate

# 4. Установить зависимости
pip install -r requirements.txt

# 5. Запустить сервер
python manage.py runserver
````
---
## 🚀 Откройте в браузере:
- http://127.0.0.1:8000/ - главная страница

- http://127.0.0.1:8000/contacts/ - контакты
---
## 🎨 Особенности интерфейса
- Главная страница с приветствием

- Страница контактов с:

  - Адресом компании

  - Контактными данными

  - Формой обратной связи

- Адаптивный дизайн на Bootstrap 5

Чистый и современный UI
---
## 📁 Структура проекта
```
django-catalog/
├── catalog/              # Основное приложение
│   ├── templates/        # Шаблоны
│   │   ├── base.html     # Базовый шаблон
│   │   ├── home.html     # Главная страница  
│   │   └── contacts.html # Страница контактов
│   ├── urls.py           # Маршруты приложения
│   └── views.py          # Контроллеры
├── config/               # Настройки проекта
├── venv/                 # Виртуальное окружение
├── .gitignore           # Игнорируемые файлы
└── README.md            # Этот файл
```
---
## 🛠 Технологии
| Технология       | Описание          |
|:----------------:|:-----------------:|
| 🐍 Python 3.10+  | Основной язык     |
| 🎭 Django 4.2+   | Веб-фреймворк     |
| 🎨 Bootstrap 5   | Стилизация        |
| 🗃️ SQLite       | База данных       |
---

###### Документация:
- Дополнительную информацию о структуре проекта и API можно найти в [GitHab](https://github.com/Umelyantsev-Vasily/hom_work_django)

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).
