from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SubmitField, URLField)
from wtforms.validators import (DataRequired, Length,
                                Optional, URL)


class LinkForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'), Length(1, 128),
            URL(message='Введите корректный URL')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16, message='Выберите ссылку короче 16 символов'),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
