import random
import re
import string
from http import HTTPStatus


from flask import (abort, flash, redirect,
                   render_template, url_for)
from sqlalchemy import exists

from . import app, db
from .forms import LinkForm
from .models import URLMap


def generate_short_id():
    symbols = f'{string.digits}{string.ascii_letters}'
    while True:
        short = ''.join(random.choice(symbols) for _ in range(6))
        if not find_short_duplicate(short):
            return short


def find_short_duplicate(short):
    return db.session.query(exists().where(URLMap.short == short)).scalar()


def check_custom_id(short_id):
    return re.fullmatch(r'[A-Za-z0-9]{1,16}$', short_id)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        if form.custom_id.data:
            short = form.custom_id.data
            if not check_custom_id(short):
                flash('В короткой ссылке можно использовать только строчные '
                      'и прописные латинские буквы и цифры 0-9. ')
                return render_template('index.html', form=form)
            if find_short_duplicate(short):
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)
        if not form.custom_id.data:
            short = generate_short_id()
        url_map = URLMap(original=form.original_link.data,
                         short=short)
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
    abort(HTTPStatus.NOT_FOUND)
