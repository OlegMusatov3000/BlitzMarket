# Blitz Market service
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Асинхронность](https://img.shields.io/badge/-Асинхронность-464646?style=flat-square&logo=Асинхронность)]()
[![Cookies](https://img.shields.io/badge/-Cookies-464646?style=flat-square&logo=Cookies)]()
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat-square&logo=JWT)]()
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat-square&logo=Alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=Redis)](https://redis.io/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?style=flat-square&logo=uvicorn)](https://www.uvicorn.org/)
[![Gunicorn](https://img.shields.io/badge/-Gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)

## Описание
В этом проекте реализован Api Сервис по размещению объявлений. Объявления могут быть разных видов (продажа, покупка, оказание услуг).
Основные роли системы: пользователь, администратор.

## Изучить документацию и протестировать сервис вы можете по адресу: http://localhost:8000/docs после выполнения всех инструкций по развертыванию приложения локально

### Возможности неавторизованного пользователя:
- Регистрация
- Просмотр списка объявлений
- Детальный просмотр одного объявления
- Просмотр комментариев объявлений
- Просмотр отзывов на объявление

### Возможности пользователя:
- Регистрация
- Вход в систему
- Выход из системы
- Размещение объявления
- Просмотр списка объявлений
- Детальный просмотр одного объявления
- Удаление своего объявления
- Комментирование объявлений
- Просмотр комментариев объявлений
- Жалоба на объявление
- Отзыв на объявление
- Просмотр отзывов на объявление

### Возможности администратора:
- Все выше перечисленное
- Удаление комментариев в любой группе объявлений 
- Назначение пользователя администратором
- Бан/разбан пользователей
- Перемещение объявлений из одной группы в другую

### Дополнительный функционал:
- Серверная пагинация
- Фильтрация объявлений 
- Сортировка записей
- Кеширование с помощью Redis
- Авторизация с помощью JWT-токена
- Сборка проекта в докер-образ
- Настройка логгера(терминал)
- При критических ошибках отправление ошибки в телеграмм чат

#### Технологии

- Python 3.10
- FastAPI
- Асинхронность
- Cookies
- JWT
- Alembic
- SQLAlchemy
- Redis
- Docker
- PostgreSQL
- Asyncpg
- Uvicorn
- Gunicorn

### Как запустить проект:

Для запуска необходим установленный Docker проверить его работоспособность вы можете используя команду:

```
docker --version
```

Если в логах появится примерно такая надпись, то все ок и можно двигаться дальше:

```
Docker version 24.0.6, build ed223bc
```

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:OlegMusatov3000/BlitzMarket.git
```

Перейдите в основную директорию проекта 

```
cd BlitzMarket
```
В файле .env_copy находится инструкция по заполнению секретных данных для проекта.
После выполнения этих инструкций убедитесь что ранее вы отправляли сообщение вашему Телеграм боту иначе он не сможет отправлять вам ошибки проекта

Запустите контейнеры Docker с помощью утилиты для оркестрации Docker Compose:

```
docker compose up -d
```

Откройте в браузере страницу http://localhost:8000/docs и проверьте, что страница доступна

Далее вы можете протестировать проект. При возникновении критической ошибки бот отправит сообщение на указанный TELEGRAM_CHAT_ID.

Для остановки и удаления всех контейнеров:

```
docker compose down
```

### Небольшое примечание

Если в процессе запуска и тестирования возникли проблемы, пожалуйста свяжитесь со мной (контакты ниже) для устранения ошибок и решения проблем с запуском

### Автор проекта 
- Олег Мусатов
- Tg: @OlegMusatov