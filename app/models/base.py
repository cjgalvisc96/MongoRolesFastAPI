from datetime import datetime

from umongo import Document, fields

from app.core.db import mongo_db


@mongo_db.db.register
class Base(Document):
    is_active = fields.BooleanField(default=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        abstract = True

    def pre_insert(self):
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def pre_update(self):
        self.updated_at = datetime.utcnow()
