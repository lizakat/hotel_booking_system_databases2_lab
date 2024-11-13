from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from models import db, Room, Client, Booking, BookingStatus, Service  # Предполагается, что модель Room определена в models.py
from forms import RoomForm, ClientForm, BookingForm, BookingStatusForm, ServiceForm  # Предполагается, что RoomForm определен в forms.py
from flask_migrate import Migrate
from sqlalchemy import text  # Импорт text
from datetime import datetime
import os
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/BSUIR?options=-csearch_path=hotel'
app.config['SECRET_KEY'] = 'supersecretkey'
#app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
migrate = Migrate(app, db)

# Главная страница - редирект на список комнат
@app.route('/')
def index():
    return redirect(url_for('booking_list'))


@app.route('/upload_sql', methods=['POST'])
def upload_sql():
    sql_file = request.files.get('sql_file')
    if not sql_file:
        flash('Файл не выбран.')
        return redirect(url_for('index'))
    
    if not sql_file.filename.endswith(('.txt', '.sql')):
        flash('Неподдерживаемый формат файла. Загрузите файл .txt или .sql')
        return redirect(url_for('index'))

    try:
        # Чтение SQL-запросов из файла
        sql_commands = sql_file.read().decode('utf-8')
        
        # Выполнение SQL-запросов в транзакции
        with db.engine.begin() as connection:  # begin() автоматически коммитит при завершении блока
            for command in sql_commands.split(';'):
                command = command.strip()
                if command:  # Игнорируем пустые строки
                    connection.execute(text(command))
        
        flash('SQL-запросы успешно выполнены!')
    except Exception as e:
        flash(f'Ошибка выполнения SQL-запросов: {str(e)}')
    return redirect(url_for('index'))

# Отображение и добавление новых комнат
@app.route('/rooms', methods=['GET', 'POST'])
def room_list():
    rooms = Room.query.order_by(Room.number).all()
    form = RoomForm()
    
    if form.validate_on_submit():  # Обработка формы добавления новой комнаты
        room = Room(
            number=form.number.data,
            bed_capacity=form.bed_capacity.data,
            price_per_night=form.price_per_night.data
        )
        db.session.add(room)
        db.session.commit()
        flash('Комната успешно добавлена!')
        return redirect(url_for('room_list'))

    return render_template('room_list.html', rooms=rooms, form=form)

# Удаление нескольких комнат
@app.route('/rooms/delete', methods=['POST'])
def delete_rooms():
    room_ids = request.form.getlist('room_ids')
    Room.query.filter(Room.room_id.in_(room_ids)).delete(synchronize_session=False)
    db.session.commit()
    flash('Комнаты успешно удалены!')
    return redirect(url_for('room_list'))

@app.route('/rooms/update_field', methods=['POST'])
def update_room_field():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data received."}), 400

    print("Data received for update:", data)  # Логируем входящие данные

    for update in data:
        room_id = update.get("room_id")
        field = update.get("field")
        value = update.get("value")

        room = Room.query.get(room_id)
        if room and field in ['number', 'bed_capacity', 'price_per_night']:
            print(f"Updating room {room_id}: setting {field} to {value}")  # Логируем обновление
            try:
                setattr(room, field, value)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error updating room {room_id} field {field}: {e}")  # Логирование ошибки
                return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True})

@app.route('/clients', methods=['GET', 'POST'])
def client_list():
    clients = Client.query.order_by(Client.name).all()
    form = ClientForm()
    
    if form.validate_on_submit():  # Обработка формы добавления нового клиента
        client = Client(
            passport_number=form.passport_number.data,
            name=form.name.data,
            phone_number=form.phone_number.data
        )
        db.session.add(client)
        db.session.commit()
        flash('Клиент успешно добавлен!')
        return redirect(url_for('client_list'))

    return render_template('client_list.html', clients=clients, form=form)

# Удаление нескольких клиентов
@app.route('/clients/delete', methods=['POST'])
def delete_clients():
    client_ids = request.form.getlist('client_ids')
    Client.query.filter(Client.client_id.in_(client_ids)).delete(synchronize_session=False)
    db.session.commit()
    flash('Клиенты успешно удалены!')
    return redirect(url_for('client_list'))

# Обновление полей клиента
@app.route('/clients/update_field', methods=['POST'])
def update_client_field():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data received."}), 400

    print("Data received for update:", data)  # Логируем входящие данные

    for update in data:
        client_id = update.get("client_id")
        field = update.get("field")
        value = update.get("value")

        client = Client.query.get(client_id)
        if client and field in ['passport_number', 'name', 'phone_number']:
            print(f"Updating client {client_id}: setting {field} to {value}")  # Логируем обновление
            try:
                setattr(client, field, value)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error updating client {client_id} field {field}: {e}")  # Логирование ошибки
                return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True})

@app.route('/bookings', methods=['GET', 'POST'])
def booking_list():
    bookings = db.session.query(Booking, Room, BookingStatus).\
        join(Room, Room.room_id == Booking.room_id).\
        join(BookingStatus, BookingStatus.status_id == Booking.status_id).\
        order_by(Booking.booking_date).all()

    form = BookingForm()
    # Установка доступных комнат в поле room_id
    form.room_id.choices = [(room.room_id, room.number) for room in Room.query.all()]
    # Установка статусов бронирования в поле status_id
    form.status_id.choices = [(status.status_id, status.status_name) for status in BookingStatus.query.all()]


    # Если редактируем существующее бронирование, подставляем данные в форму
    if request.args.get('booking_id'):
        booking = Booking.query.get(request.args.get('booking_id'))
        form.room_id.data = booking.room_id
        form.status_id.data = booking.status_id
        form.booking_date.data = booking.booking_date
        form.check_in_date.data = booking.check_in_date
        form.check_out_date.data = booking.check_out_date

    if form.validate_on_submit():
        # Если создаем новое бронирование
        booking = Booking(
            booking_date=form.booking_date.data,
            check_in_date=form.check_in_date.data,
            check_out_date=form.check_out_date.data,
            room_id=form.room_id.data,
            status_id=form.status_id.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Бронирование успешно добавлено!')
        return redirect(url_for('booking_list'))

    return render_template('booking_list.html', bookings=bookings, form=form)


@app.route('/bookings/delete', methods=['POST'])
def delete_bookings():
    booking_ids = request.form.getlist('booking_ids')
    if booking_ids:
        Booking.query.filter(Booking.booking_id.in_(booking_ids)).delete(synchronize_session=False)
        db.session.commit()
        flash('Бронирования успешно удалены!')
    else:
        flash('Не выбрано ни одно бронирование для удаления.', 'error')
    return redirect(url_for('booking_list'))


@app.route('/bookings/update_field', methods=['POST'])
def update_booking_field():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data received."}), 400

    print("Data received for update:", data)  # Логируем входящие данные

    try:
        for update in data:
            booking_id = update.get("booking_id")
            field = update.get("field")
            value = update.get("value")

            booking = Booking.query.get(booking_id)
            
            if not booking:
                print(f"Booking with ID {booking_id} not found.")
                continue

            # Обработка каждого поля в зависимости от типа
            if field == 'room_id':
                # Найти room_id по номеру комнаты
                room = Room.query.filter_by(number=value).first()
                if room:
                    booking.room_id = room.room_id
                    print(f"Setting booking {booking_id} room_id to {room.room_id} based on room number {value}")
                else:
                    print(f"Room with number {value} not found.")
                    return jsonify({"success": False, "error": f"Room with number {value} not found"}), 404

            elif field == 'status_id':
                # Проверка, передан ли `status_name` или `status_id`
                if isinstance(value, str):  # Если значение передано как имя статуса
                    status = BookingStatus.query.filter_by(status_name=value).first()
                else:  # Если передан идентификатор
                    status = BookingStatus.query.filter_by(status_id=value).first()
                    
                if status:
                    booking.status_id = status.status_id
                    print(f"Setting booking {booking_id} status_id to {status.status_id}")
                else:
                    print(f"Status with value {value} not found.")
                    return jsonify({"success": False, "error": f"Status with value {value} not found"}), 404

            elif field in ['booking_date', 'check_in_date', 'check_out_date']:
                # Обработка даты: преобразование строки в datetime.date
                try:
                    date_value = datetime.strptime(value, "%Y-%m-%d").date()
                    setattr(booking, field, date_value)
                    print(f"Updating booking {booking_id}: setting {field} to {date_value}")
                except ValueError:
                    print(f"Invalid date format for {field}: {value}")
                    return jsonify({"success": False, "error": f"Invalid date format for {field}"}), 400

        # Совершение коммита после всех изменений
        db.session.commit()
        print("All changes committed successfully.")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating booking fields: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True})

# Отображение списка услуг и добавление новой
@app.route('/services', methods=['GET', 'POST'])
def service_list():
    services = Service.query.order_by(Service.type).all()
    form = ServiceForm()
    
    if form.validate_on_submit():  # Обработка формы добавления новой услуги
        service = Service(
            type=form.type.data,
            cost=form.cost.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Услуга успешно добавлена!')
        return redirect(url_for('service_list'))

    return render_template('service_list.html', services=services, form=form)

# Удаление нескольких услуг
@app.route('/services/delete', methods=['POST'])
def delete_services():
    service_ids = request.form.getlist('service_ids')
    Service.query.filter(Service.service_id.in_(service_ids)).delete(synchronize_session=False)
    db.session.commit()
    flash('Услуги успешно удалены!')
    return redirect(url_for('service_list'))

# Обновление отдельных полей услуги
@app.route('/services/update_field', methods=['POST'])
def update_service_field():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data received."}), 400

    print("Data received for update:", data)  # Логируем входящие данные

    for update in data:
        service_id = update.get("service_id")
        field = update.get("field")
        value = update.get("value")

        service = Service.query.get(service_id)
        if service and field in ['type', 'cost']:
            print(f"Updating service {service_id}: setting {field} to {value}")  # Логируем обновление
            try:
                setattr(service, field, value)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error updating service {service_id} field {field}: {e}")  # Логирование ошибки
                return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True})

@app.route('/booking_statuses', methods=['GET', 'POST'])
def status_list():
    statuses = BookingStatus.query.all()
    form = BookingStatusForm()

    if form.validate_on_submit():
        status = BookingStatus(
            status_name=form.status_name.data
        )
        db.session.add(status)
        db.session.commit()
        flash('Статус бронирования успешно добавлен!')
        return redirect(url_for('status_list'))

    return render_template('status_list.html', statuses=statuses, form=form)

@app.route('/booking_statuses/delete', methods=['POST'])
def delete_statuses():
    status_ids = request.form.getlist('status_ids')
    BookingStatus.query.filter(BookingStatus.status_id.in_(status_ids)).delete(synchronize_session=False)
    db.session.commit()
    flash('Статусы успешно удалены!')
    return redirect(url_for('status_list'))

@app.route('/booking_statuses/update_field', methods=['POST'])
def update_status_field():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data received."}), 400

    for update in data:
        status_id = update.get("status_id")
        field = update.get("field")
        value = update.get("value")

        status = BookingStatus.query.get(status_id)
        if status and field == 'status_name':
            try:
                setattr(status, field, value)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": True})


# Функция для генерации файла из данных таблицы
def generate_file(table_name, file_format):
    # Извлекаем данные из базы данных на основе названия таблицы
    if table_name == 'clients':
        query = Client.query.all()
    elif table_name == 'rooms':
        query = Room.query.all()
    elif table_name == 'bookings':
        query = Booking.query.all()
    elif table_name == 'services':
        query = Service.query.all()
    elif table_name == 'statuses':
        query = BookingStatus.query.all()
    else:
        flash("Неизвестная таблица.")
        return None

    # Конвертируем результаты запроса в Pandas DataFrame
    data = pd.DataFrame([row.__dict__ for row in query])
    data = data.drop(columns=['_sa_instance_state'])  # Удаление служебной колонки SQLAlchemy

    # Сохраняем файл в нужном формате
    filename = f"{table_name}_{file_format}.{file_format}"
    filepath = os.path.join("downloads", filename)  # Путь для сохранения

    # Создаем папку "downloads", если ее нет
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # Сохраняем файл в зависимости от формата
    if file_format == 'csv':
        data.to_csv(filepath, index=False)
    elif file_format == 'xlsx':
        data.to_excel(filepath, index=False)
    elif file_format == 'json':
        data.to_json(filepath, orient='records')
    else:
        flash("Неподдерживаемый формат файла.")
        return None

    return filename

# Маршрут для скачивания файла
@app.route('/download/<table_name>/<file_format>')
def download_file(table_name, file_format):
    # Генерируем файл для указанной таблицы и формата
    filename = generate_file(table_name, file_format)
    
    # Если файл был успешно сгенерирован, отправляем его пользователю
    if filename:
        return send_from_directory(directory='downloads', path=filename, as_attachment=True)

    flash("Ошибка при генерации файла.")
    return redirect(url_for('index'))


if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)  # Создаем директорию для скачиваемых файлов, если она не существует
    app.run(debug=True)

