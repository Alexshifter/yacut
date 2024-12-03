from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import (check_custom_id,
                    check_exist_short_dublicate,
                    short_id_generator)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    if not request.data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' in data and data['custom_id']:
        if check_exist_short_dublicate(data['custom_id']):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        if not check_custom_id(data['custom_id']):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
    else:
        data['custom_id'] = short_id_generator()
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_link(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is not None:
        return jsonify({'url': url.to_dict().get('url')}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
