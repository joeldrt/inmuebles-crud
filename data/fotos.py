import mongoengine
import datetime

import data.mongo_digiall_utils as mongo_utils


class Foto(mongoengine.Document):
    fecha_carga = mongoengine.DateTimeField(default=datetime.datetime.now)
    nombre = mongoengine.StringField(required=True)
    data_base_64 = mongoengine.StringField(required=True)
    content_type = mongoengine.StringField(required=True)
    inmueble_id = mongoengine.StringField(required=True)

    def to_dict(self):
        return mongo_utils.mongo_to_dict(self)

    meta = {
        'db_alias': 'core',
        'collection': 'fotos'
    }
