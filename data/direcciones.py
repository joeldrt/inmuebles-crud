import mongoengine


class Direccion(mongoengine.EmbeddedDocument):
    calle = mongoengine.StringField(required=True)
    num_exterior = mongoengine.StringField()
    num_interior = mongoengine.StringField()
    colonia = mongoengine.StringField()
    municipio = mongoengine.StringField()
    estado = mongoengine.StringField()
    pais = mongoengine.StringField()
