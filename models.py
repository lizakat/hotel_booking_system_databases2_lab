from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer, primary_key=True)  # Изменено на room_id
    number = db.Column(db.Integer, unique=True, nullable=False)  # Номер комнаты, уникальный
    bed_capacity = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Numeric(7, 2), nullable=False)  # Увеличена точность

class BookingStatus(db.Model):
    __tablename__ = 'booking_status'
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(30), unique=True, nullable=False)

class Booking(db.Model):
    __tablename__ = 'booking'
    booking_id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.Date, nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'), nullable=False)  # Изменено на room_id
    status_id = db.Column(db.Integer, db.ForeignKey('booking_status.status_id'), nullable=False)
 

    room = db.relationship('Room', backref='bookings')
    status = db.relationship('BookingStatus', backref='bookings')

class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True)  # Добавлено поле client_id как PRIMARY KEY
    passport_number = db.Column(db.String(9), unique=True, nullable=False)  # Исправлено на passport_number
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(13), nullable=False)

class Service(db.Model):
    __tablename__ = 'service'
    service_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), nullable=False)
    cost = db.Column(db.Numeric(7, 2), nullable=False)

class BookingClient(db.Model):
    __tablename__ = 'booking_client'
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), primary_key=True)  # Исправлено на passport_number

class BookingService(db.Model):
    __tablename__ = 'booking_service'
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), primary_key=True)
