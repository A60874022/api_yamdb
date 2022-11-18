### 1 Описание

Данная работа сделана на основании [технического задания](https://practicum.yandex.ru/learn/backend-developer/courses/8a4693f6-fa0e-4ab0-babd-a13453ad99c0/sprints/74395/topics/5fa48712-5641-431b-bea2-ba4e79c6a41a/lessons/f58be873-5c4f-44d6-bcc6-92255ae69ab2/),
Приложение yatube представляет собой социальную сеть, в которой люди могут создавать свои посты, 
оставлять комментарии к постам. В данной работе требуется написать API данной сети, которая позволить общаться с данным приложением. Разрабатываемый программный код выделен в приложение API

### 2 Установка

# 1 Клонировать репозиторий и перейти в него в командной строке:
git clone https://git@github.com:A60874022/api_yatube.git
cd 9

# 2 Cоздать и активировать виртуальное окружение:

python -m venv venv

venv/Scripts/activate

python -m pip install --upgrade pip


# 3 Установить зависимости из файла requirements.txt:

pip install -r requirements.txt

# 4 Выполнить миграции:

python manage.py migrate

# 5 Запустить проект:

python manage.py runserver


### 3 Запросы к API


После запуска проекта документация и примеры запросов приведены адресу http://127.0.0.1:8000/redoc/ 


