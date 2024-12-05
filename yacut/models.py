from datetime import datetime

from flask import url_for

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(short_link=url_for(
            'redirect_view',
            short_id=self.short,
            _external=True),
            url=self.original
        )

    def from_dict(self, data):

        self.short = data['custom_id']
        self.original = data['url']
