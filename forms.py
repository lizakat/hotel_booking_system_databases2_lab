from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class RoomForm(FlaskForm):
    #room_id = IntegerField('ID команты', validators=[DataRequired()])
    number = IntegerField('Номер комнаты', validators=[DataRequired(), NumberRange(min=101, max=3000)])
    bed_capacity = IntegerField('Вместимость', validators=[DataRequired(), NumberRange(min=1, max=6)])
    price_per_night = DecimalField('Цена за ночь', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

class BookingForm(FlaskForm):
    # booking_id = DateField('ID', validators=[DataRequired()])
    booking_date = DateField('Дата бронирования', validators=[DataRequired()])
    check_in_date = DateField('Дата заезда', validators=[DataRequired()])
    check_out_date = DateField('Дата выезда', validators=[DataRequired()])
    room_id = SelectField('Номер комнаты', coerce=int, validators=[DataRequired()])
    status_id = SelectField('Статус бронирования', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class ClientForm(FlaskForm):
    #client_id = IntegerField('ID клиента', validators=[DataRequired()])
    passport_number = StringField('Номер паспорта', validators=[DataRequired(), Length(min=9, max=9)])
    name = StringField('Имя', validators=[DataRequired()])
    phone_number = StringField('Номер телефона', validators=[Optional(), Length(min=13, max=13)])
    submit = SubmitField('Сохранить')

# Форма для таблицы hotel.service
class ServiceForm(FlaskForm):
    #service_id = IntegerField('ID услуги', validators=[Optional()])  # ID может быть не обязательным для создания новых записей
    type = StringField('Тип услуги', validators=[DataRequired(), Length(max=30)])
    cost = DecimalField('Стоимость', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    submit = SubmitField('Сохранить')

# Форма для таблицы hotel.booking_status
class BookingStatusForm(FlaskForm):
    #status_id = IntegerField('ID статуса', validators=[Optional()])  # ID также может быть не обязательным
    status_name = StringField('Название статуса', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Сохранить')