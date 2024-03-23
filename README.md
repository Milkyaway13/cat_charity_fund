# Проект QRKot

## Описание:

Проект для создания благотворительных фондов для котиков и внесения пожертвований. Просто выбери, каким котикам ты хочешь помочь!
А если какой-то фонд уже собрал необходимую сумму пожертвований, то твои деньги пойдут в фонд помощи другим котикам!

## Технологии:

* Python 3.9
* FastAPI 0.78
* SQLAlchemy 1.4
* Alembic 1.7

## Документация OpenAPI доступна по ссылке: http://127.0.0.1:8000/docs

## Установка и запуск:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Milkyaway13/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Для Linux/macOS

    ```
    source venv/bin/activate
    ```

* Для Windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Применить миграции:

```
alembic upgrade head
```

Запустить приложение:

```
uvicorn app.main:app
```


## Автор
[Боярчук Василий](https://github.com/Milkyaway13/)
