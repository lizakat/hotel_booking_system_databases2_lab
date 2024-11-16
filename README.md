# Проект управления гостиницей

Этот проект представляет собой веб-приложение для управления гостиницей, позволяющее выполнять операции с клиентами, комнатами, бронированиями и услугами. Пользователи могут добавлять, редактировать и удалять записи, а также загружать данные из SQL-файлов и генерировать отчеты в различных форматах.

## Стек технологий

- **Язык программирования**: Python
- **Веб-фреймворк**: Flask
- **База данных**: PostgreSQL
- **ORM**: SQLAlchemy
- **Фронтенд**: HTML, CSS, JavaScript
- **Библиотеки**:
  - Flask-WTF (для работы с формами)
  - Flask-Migrate (для миграций базы данных)
  - Pandas (для обработки данных)
- **Инструменты разработки**:
  - Jinja2 (для шаблонов)
  - Werkzeug (для обработки запросов)

## Установка

1. Клонируйте репозиторий:

   

2. Создайте виртуальное окружение и активируйте его:

   Для Linux/Mac:

   
   python -m venv venv
   source venv/bin/activate
   

   Для Windows:

   
   python -m venv venv
   venv\Scripts\activate
   

3. Установите зависимости:

   
   pip install -r requirements.txt
   

4. Настройте базу данных:
   - Убедитесь, что PostgreSQL установлен и запущен.
   - Создайте базу данных и настройте строку подключения в `app.py`.

5. Выполните миграции:

   
   flask db init
   flask db migrate
   flask db upgrade
   

6. Запустите приложение:

   
   flask run
   

## Функциональность

### 1. **Клиенты**
- Добавление, редактирование и удаление клиентов.
- Просмотр списка клиентов с возможностью выбора для удаления.

### 2. **Комнаты**
- Управление комнатами: добавление, редактирование и удаление.
- Просмотр и фильтрация списка комнат.

### 3. **Бронирования**
- Создание, редактирование и удаление бронирований.
- Отображение списка всех бронирований с возможностью фильтрации по статусу.

### 4. **Услуги**
- Добавление, редактирование и удаление услуг.
- Просмотр списка услуг.

### 5. **Загрузка и генерация отчетов**
- Загрузка SQL-файлов для выполнения команд.
- Генерация отчетов в форматах CSV, JSON и Excel.

## Примечания

- Для работы с приложением требуется установленный PostgreSQL.
- Приложение разработано с использованием подхода **MVC (Model-View-Controller)**, что обеспечивает четкое разделение логики приложения и представления.
- Приложение поддерживает загрузку и выполнение SQL-скриптов для удобства работы с данными.

