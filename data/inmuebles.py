import mongoengine
import datetime

from data.direcciones import Direccion

import data.mongo_digiall_utils as mongo_utils


class Inmueble(mongoengine.Document):
    fecha_registro = mongoengine.DateTimeField(default=datetime.datetime.now)

    nombre = mongoengine.StringField(required=True)

    m2_terreno = mongoengine.FloatField()
    m2_construccion = mongoengine.FloatField()

    niveles = mongoengine.IntField()
    recamaras = mongoengine.IntField()
    banos = mongoengine.FloatField()
    cajones_estacionamiento = mongoengine.IntField()
    amenidades = mongoengine.StringField()

    descripcion = mongoengine.StringField()

    precio_venta = mongoengine.DecimalField()
    precio_renta = mongoengine.DecimalField()

    direccion = mongoengine.EmbeddedDocumentField(Direccion)

    def to_dict(self):
        return mongo_utils.mongo_to_dict(self)

    meta = {
        'db_alias': 'core',
        'collection': 'inmuebles'
    }
