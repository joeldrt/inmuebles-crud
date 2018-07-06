from flask_restful import Resource, reqparse
from data.fotos import Foto
from data.inmuebles import Inmueble
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from services import foto_service, inmueble_service

parser = reqparse.RequestParser()
parser.add_argument('nombre', help='El campo no puede ser vacío', required=True, type=str)
parser.add_argument('data_base_64', help='El campo no puede ser vacío', required=True, type=str)
parser.add_argument('content_type', help='El campo no puede ser vacío', required=True, type=str)
parser.add_argument('inmueble_id', help='El campo no puede ser vacío', required=True, type=str)


class FotoCollection(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()

        foto_id_str = foto_service.persist_foto(nombre=data['nombre'],
                                                data_base_64=data['data_base_64'],
                                                content_type=data['content_type'],
                                                inmueble_id=data['inmueble_id'])

        if foto_id_str:
            return {'foto_id': foto_id_str}
        else:
            return {'message': 'La Foto no pudo ser guardada'}, 500

    # not included as publish resource
    # @jwt_required
    # def get(self):
    #     fotos = service.get_all_fotos()
    #     return fotos


class FotoItem(Resource):
    @jwt_required
    def get(self, foto_id):
        try:
            foto = foto_service.get_foto_by_id(foto_id)
        except Foto.DoesNotExist as e:
            return {'message': 'Foto con id {} no fue encontrada. mensaje del servidor: {}'
                    .format(foto_id, e.args[0])}, 404
        return foto.to_dict()

    @jwt_required
    def delete(self, foto_id):
        try:
            foto = foto_service.get_foto_by_id(foto_id)
            foto.delete()
        except Foto.DoesNotExist as e:
            return {'message': e.args[0]}, 404
        return {'message'}


class FotoItemByInmueble(Resource):
    @jwt_required
    def get(self, inmueble_id):
        try:
            inmueble_service.get_inmueble_by_id(inmueble_id)
        except Inmueble.DoesNotExist as e:
            return {'message': 'Inmueble con id {} no fue encontrado. mensaje del servidor: {}'
                    .format(inmueble_id, e.args[0])}, 404

        fotos = foto_service.get_fotos_by_inmueble_id(inmueble_id)
        return fotos
