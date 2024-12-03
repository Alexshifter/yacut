from datetime import datetime

from . import db

from flask import url_for

class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict( short_link=url_for(
            'redirect_view',
            short_id=self.short,
            _external=True), 
            url=self.original
           
        )

    def from_dict(self, data):
        data = {
            'short': data.pop('custom_id', None),
            'original': data.pop('url', None)
        }
        for field in ['original', 'short']:
            if data[field]:
                setattr(self, field, data[field])
