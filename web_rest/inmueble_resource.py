from flask_restful import Resource, reqparse
from data.inmuebles import Inmueble
from flask_jwt_extended import (jwt_required)
from services import inmueble_service as service
import shutil

from werkzeug.exceptions import BadRequest
import json

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('id')
parser.add_argument('nombre', help='El campo no puede ser vacío', required=True)
parser.add_argument('m2_terreno', type=float, help='No se pudo convertir el valor enviado')
parser.add_argument('m2_construccion', type=float, help='No se pudo convertir el valor enviado')
parser.add_argument('niveles', type=int, help='No se pudo convertir el valor enviado')
parser.add_argument('recamaras', type=int, help='No se pudo convertir el valor enviado')
parser.add_argument('banos', type=float, help='No se pudo convertir el valor enviado')
parser.add_argument('cajones_estacionamiento', type=int, help='No se pudo convertir el valor enviado')
parser.add_argument('amenidades')
parser.add_argument('descripcion')
parser.add_argument('precio_venta', type=float, help='No se pudo convertir el valor enviado')
parser.add_argument('precio_renta', type=float, help='No se pudo convertir el valor enviado')
parser.add_argument('calle')
parser.add_argument('num_exterior')
parser.add_argument('num_interior')
parser.add_argument('colonia')
parser.add_argument('municipio')
parser.add_argument('estado')
parser.add_argument('pais')
parser.add_argument('tags', type=list, help='No se pudo convertir la lista')
parser.add_argument('fotos', type=list, help='No se pudo convertir la lista')


class AgregarInmueble(Resource):
    @jwt_required
    def post(self):
        try:
            data = parser.parse_args()
        except BadRequest as br:
            br_data = br.data
            br_message = br_data['message']
            return {'message': '{} - {}'.format(br.description, json.dumps(br_message))}, br.code

        new_inmueble = service.persist_inmueble(nombre=data['nombre'],
                                                m2_terreno=data['m2_terreno'],
                                                m2_construccion=data['m2_construccion'],
                                                niveles=data['niveles'],
                                                recamaras=data['recamaras'],
                                                banos=data['banos'],
                                                cajones_estacionamiento=data['cajones_estacionamiento'],
                                                amenidades=data['amenidades'],
                                                descripccion=data['descripcion'],
                                                precio_venta=data['precio_venta'],
                                                precio_renta=data['precio_renta'],
                                                calle=data['calle'],
                                                num_exterior=data['num_exterior'],
                                                num_interior=data['num_interior'],
                                                colonia=data['colonia'],
                                                municipio=data['municipio'],
                                                estado=data['estado'],
                                                pais=data['pais'],
                                                tags=data['tags'],
                                                fotos=data['fotos'],
                                                inmueble_id=None)

        if new_inmueble:
            return new_inmueble.to_dict()
        else:
            return {'message': 'El Inmueble no pudo ser guardado'}, 500


class ObtenerTodosLosInmuebles(Resource):
    def get(self):
        inmuebles = service.get_all_inmuebles()
        return inmuebles


class BorrarInmueble(Resource):
    @jwt_required
    def delete(self, inmueble_id):
        try:
            inmueble = service.get_inmueble_by_id(inmueble_id)
            inmueble.delete()
            # borramos el directorio estático también
            shutil.rmtree('static/{}'.format(inmueble_id), ignore_errors=True)
        except Inmueble.DoesNotExist as e:
            return {'message': e.args[0]}, 404
        return {'message': 'Inmueble con id: {} borrado exitosamente'.format(inmueble.id)}


class EditarInmueble(Resource):
    @jwt_required
    def put(self):
        try:
            data = parser.parse_args()
        except BadRequest as br:
            br_data = br.data
            br_message = br_data['message']
            return {'message': '{} - {}'.format(br.description, json.dumps(br_message))}, br.code

        inmueble = service.get_inmueble_by_id(data['id'])

        if inmueble is None:
            return {'message': 'Error al editar, Id de inmueble inválido'}, 400

        inmueble.nombre = data['nombre']
        inmueble.m2_terreno = data['m2_terreno']
        inmueble.m2_construccion = data['m2_construccion']
        inmueble.niveles = data['niveles']
        inmueble.recamaras = data['recamaras']
        inmueble.banos = data['banos']
        inmueble.cajones_estacionamiento = data['cajones_estacionamiento']
        inmueble.amenidades = data['amenidades']
        inmueble.descripcion = data['descripcion']
        inmueble.precio_venta = data['precio_venta']
        inmueble.precio_renta = data['precio_renta']
        inmueble.calle = data['calle']
        inmueble.num_exterior = data['num_exterior']
        inmueble.num_interior = data['num_interior']
        inmueble.colonia = data['colonia']
        inmueble.municipio = data['municipio']
        inmueble.estado = data['estado']
        inmueble.pais = data['pais']

        edited_inmueble = inmueble.save()

        if edited_inmueble:
            return edited_inmueble.to_dict()
        else:
            return {'message': 'El Inmueble no pudo ser editado'}, 500
