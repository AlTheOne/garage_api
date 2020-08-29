# Тестовое задание HuskyJam

Создать API сервис для записи в автомастерскую на диагностику.

# Запуск проект с помощью Docker

Создаём и накатываем миграции:
```
> docker-compose run web python manage.py makemigrations
> docker-compose run web python manage.py migrate
```

Запускаем процедуру создания Супер пользователя:
```
> docker-compose run web python manage.py createsuperuser
```

Запускаем приложение:
```
> docker-compose up -d
```

Сайт доступен по адресу: `http://127.0.0.1` 

*Внимание! Для удобства просмотра приложение запускается с DEV настройками.*

# Запуск тестов

```
> docker-compose run web python manage.py pytest
```