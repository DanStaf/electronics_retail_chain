# Online platform for the electronics retail chain

## Used technologies:
- Python 3.8+
- Django 3+
- DRF 3.10+
- PostgreSQL 10+

## Description:

Веб-приложение с API-интерфейсом и админ-панелью, базой данных PostgreSQL.

Реализована модель сети по продаже электроники.

Сеть представляет собой иерархическую структуру из трех уровней:
- завод;
- розничная сеть;
- индивидуальный предприниматель.

Каждое звено сети ссылается только на одного поставщика оборудования 
(не обязательно предыдущего по иерархии). Важно отметить, что уровень 
иерархии определяется не названием звена, а отношением к остальным 
элементам сети, т. е. завод всегда находится на уровне 0, а если 
розничная сеть относится напрямую к заводу, минуя остальные звенья, 
ее уровень — 1.

### Модели:

1. User
2. Product
3. Company (каждое звено сети)

### На админ-панели выведены созданные объекты.

На странице объекта сети добавлены:

- ссылка на «Поставщика»;
- фильтр по названию города;
- admin action, очищающий задолженность перед поставщиком у выбранных объектов.

### С помощью DRF, создан набор представлений:
- CRUD для модели поставщика (без возможности обновления через API поля «Задолженность перед поставщиком»).
- фильтрация объектов по определенной стране.
- Только активные сотрудники имеют доступ к API.

## How it works:
- Установить зависимости
- Выполнить миграции
- Запуск веб-приложения командой `python manage.py runserver`
