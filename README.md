# task_manager

## Консольное приложение для управления задачами.

Консольное приложение task_manager позволяет создавать, искать, редактировать и удалять задачи.
Данные хранятся в json-формате.

## **Запуск проекта в dev-режиме**

Клонировать репозиторий:

```
git clone https://github.com/Paradaise1/task_manager.git
```

```
cd task_manager
```

Создать и активировать виртуальное окружение (если планируете использовать тесты)

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Для запуска проекта используйте команду:

```
python main.py
```

Для запуска тестов к проекту используйте команду:

```
pytest
```