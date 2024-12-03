import random
import string

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import LinkForm
from .models import URLMap


def short_id_generator():
    symbols = string.digits + string.ascii_letters
    while True:
        """Генерируем ссылку и проверяем есть ли дубликат в базе."""
        short = ''.join(random.choice(symbols) for _ in range(6))
        if not check_exist_short_dublicate(short):
            return short


def check_exist_short_dublicate(short):
    return (URLMap.query.filter_by(short=short).first())


def create_obj_for_db(original_link, short_id):
    return URLMap(original=original_link,
                  short=short_id)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            short = short_id_generator()
        else:
            short = form.custom_id.data
            if check_exist_short_dublicate(short):
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html',
                                       form=form)
        url_map = create_obj_for_db(form.original_link.data, short)
        
        db.session.add(url_map)
        db.session.commit()
        flash('Ваша новая ссылка готова:')
        return render_template('index.html', form=form, new_link=url_for(
            'redirect_view',
            short_id=url_map.short,
            _external=True)
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_view(short_id):
    obj = URLMap.query.filter_by(short=short_id).first()
    if obj is not None:
        return redirect(obj.original)
    abort(404)
