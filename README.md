# Тестовое задание HuskyJam

Создать API сервис для записи в автомастерскую на диагностику.

# Подготовка

Создаём и накатываем миграции:
```
> docker-compose run web python manage.py makemigrations
> docker-compose run web python manage.py migrate
```

Запускаем процедуру создания Супер пользователя:
```
> docker-compose run web python manage.py createsuperuser
```

# Запуск проект с помощью Docker

Запускаем приложение:
```
> docker-compose up -d
```

Сайт доступен по адресу: `http://127.0.0.1` 

*Внимание! Для удобства просмотра приложение запускается с DEV настройками.*

# Запуск тестов

```
> docker-compose run web pytest
```

*Внимание! Перед запуском тестов необходимо выполнить [Подготовку](https://github.com/AlTheOne/garage_api/#%D0%BF%D0%BE%D0%B4%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%BA%D0%B0)*
