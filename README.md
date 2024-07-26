## Тестовое задание Python Developer

**Сделать web приложение, оно же сайт, где пользователь вводит название города, и получает прогноз погоды в этом городе на ближайшее время.**

### Установка
- Сбор контейнеров
```commandline
docker-compose up -d --build
```
- Локально
```commandline
pip install -r requirements.txt
```
```commandline
python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000
```
### Приложение
- Получить доступ к приложению
```djangourlpath
http://localhost:8000/
```

### Технологии
- django
- requests
- ajax

### Реализовано
- написаны тесты
- всё это помещено в докер контейнер
- при повторном посещении сайта будет предложено посмотреть погоду в городе, в котором пользователь уже смотрел ранее
- будет сохраняться история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город
