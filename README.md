# Sbertech

## Project structure

```
├──sbertech
   │   .pre-commit-config.yaml # хуки для валидации кода линтерами и форматерами
   │   docker-compose.yaml
   │   Dockerfile
   │   generate-openapi-spec.py # автогенерация openapi спецификации. может использоваться для code-first подхода 
   │                              или сверки с ручной версией
   │   run-container.sh
   │   poetry.lock # стабильная альтернатива requirements.txt
   │   poetry.toml    
   │   pyproject.toml
   │
   ├───backend
   │   │   app.py
   │   │
   │   ├───config
   │   │      app.py
   │   │      logger.py
   │   │             
   │   ├───domain # логика
   │   │      deposits.py
   │   │
   │   ├───pydantic_models # модели для запросов и ответов
   │   │   │  common.py
   │   │   │
   │   │   ├───v1
   │   │   │     deposits.py           
   │   │   └───v2
   │   │         deposits.py     
   │   │
   │   └───routers # эндпоинты
   │       │ 
   │       ├───v1
   │       │     deposits.py        
   │       └───v2
   │             deposits.py  
   │           
   ├───openapi
   │       api-references.yml
   │
   └───tests
           test_*.json # данные к тестам
           test_*.py
```

## V1 vs V2

В отсутствии возможности дискутировать по поводу вариантов реализации различных аспектов проекта - 
я решил сделать апишную часть двумя способами: максимально приближенным к тексту тестового и альтернативный.

### Отличия

- #### POST vs GET
    Если я правильно понял, то в задании предлагается отправлять json, то есть использовать POST и body. 
    Мне кажется более подходящим является GET, так как операция является индемпотентной и безопасной.
    Из этого же следует, что никакие ресурсы не создаются.
- #### request/response date format
    В задании предлагается формат даты '%d.%m.%Y', что, кажется лишним усложением, так как данный формат не
    является дефолтно поддерживаемым и требует явной конвертации как в момент принятия запроса так и в момент
    его отправки. Отказываемся (я все таки его оставил) от format: date в спеке.
- #### response json format
    Предложен вариант словаря с key = дата и value = сумма на счету. Такой динамический ключ сложно документировать.
    По сути только в комментарии можно дать наводку фронту или юзеру, что ожидается в ключе. Это усложняет парсинг.
    Во второй версии я решил использовать следующую структуру:
    ```
    [
      {
        "date": "2022-12-20",
        "amount": 123123
      },
      {
        "date": "2023-1-20",
        "amount": 123456
      }
    ]
    ```
    Она позволяет четко зафиксировать статические названия полей и их типы.
- #### Validation Error response
    Я сделал только предложеный вариант, но стоит упомянуть. Он немного усложняет реализацию в fastapi, так как fastapi 
    автоматически добавляет 422 response ко всем эндпоинтам на случай ошибки валидации. Пришлось его ручками удалять +
    pydantic валидирует все поля, а не падает на первом, поэтому ошибку надо склеивать, а изначальный json достаточно 
    подробный.

### Start app
  ```
    docker-compose up --build
  ```
  
  После запуска перейдите по ссылке [localhost:5000](http://localhost:5000)

### Pytest
  Выполните данную команду в корне проекта для просмотра покрытия (актуальное покрытие выведено ниже)
  ```
  poetry run pytest --cov=backend
  
  Name                                     Stmts   Miss  Cover
------------------------------------------------------------
backend\__init__.py                          2      0   100%
backend\app.py                              40     14    65%
backend\config\__init__.py                   6      0   100%
backend\config\app.py                       30      3    90%
backend\config\logger.py                    13      0   100%
backend\domain\__init__.py                   0      0   100%
backend\domain\deposits.py                  70      2    97%
backend\pydantic_models\__init__.py          0      0   100%
backend\pydantic_models\common.py            5      0   100%
backend\pydantic_models\v1\__init__.py       0      0   100%
backend\pydantic_models\v1\deposits.py      21      0   100%
backend\pydantic_models\v2\__init__.py       0      0   100%
backend\pydantic_models\v2\deposits.py      18      0   100%
backend\routers\__init__.py                  0      0   100%
backend\routers\v1\__init__.py               4      0   100%
backend\routers\v1\deposits.py              11      0   100%
backend\routers\v2\__init__.py               4      0   100%
backend\routers\v2\deposits.py              11      0   100%
------------------------------------------------------------
TOTAL                                      235     19    92%

  ```