import mongoengine
import datetime

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

    precio_venta = mongoengine.FloatField()
    precio_renta = mongoengine.FloatField()

    calle = mongoengine.StringField(required=True)
    num_exterior = mongoengine.StringField()
    num_interior = mongoengine.StringField()
    colonia = mongoengine.StringField()
    municipio = mongoengine.StringField()
    estado = mongoengine.StringField()
    pais = mongoengine.StringField()

    tags = mongoengine.ListField(mongoengine.StringField(), default=[])

    fotos = mongoengine.ListField(mongoengine.StringField(), default=[])

    status = mongoengine.IntField(required=True, default=0)

    def to_dict(self):
        return mongo_utils.mongo_to_dict(self)

    meta = {
        'db_alias': 'core',
        'collection': 'inmuebles'
    }
