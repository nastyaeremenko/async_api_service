# API для онлайн-кинотеатра

### Описание
Проект отображает данные по фильмам, жанрам, актерам, режиссерам и сценаристам.

После запуска кода документацию по API можно посмотреть по ссылке: http://localhost/api/openapi

### Технологии
- Python 3.9 
- FastAPI 0.75.0 
- ElasticSearch 7.14.0

### Запуск проекта
- Скачайте проект с ETL https://github.com/evdrug/new_admin_panel_sprint_3
- Заполните файл .env в соответствии с .example.env
- Перейдите в папку проекта new_admin_panel_sprint_3 и запустите его (название контейнера должно быть new_admin_panel_sprint_3):
```
docker-compose up -d
```
- Скачайте и запустите данный проект (значение параметров .env должны совпадать с .env из ранее запущенного проект):
```
docker-compose up -d
```
### Запуск тестов
- Запуск локального окружения для тестов
```
docker-compose -f tests/functional/docker-compose.yml up -d
```
- Запуск тестов в контейнере
```
docker-compose -f tests/functional/docker-compose-tests.yml up --build
```
- Запуск локальных тестов
```
pytest tests/functional/src
```
### Авторы
Евгений Д., Анастасия Еременко