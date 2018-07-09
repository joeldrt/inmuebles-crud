from flask_restful import Resource, reqparse
from data.inmuebles import Inmueble
from flask_jwt_extended import (jwt_required)
from services import inmueble_service as service

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('nombre', help='El campo no puede ser vacío', required=True)
parser.add_argument('m2_terreno', type=float)
parser.add_argument('m2_construccion', type=float)
parser.add_argument('niveles', type=int)
parser.add_argument('recamaras', type=int)
parser.add_argument('banos', type=float)
parser.add_argument('cajones_estacionamiento', type=int)
parser.add_argument('amenidades')
parser.add_argument('descripcion')
parser.add_argument('precio_venta', type=float)
parser.add_argument('precio_renta', type=float)
parser.add_argument('calle')
parser.add_argument('num_exterior')
parser.add_argument('num_interior')
parser.add_argument('colonia')
parser.add_argument('municipio')
parser.add_argument('estado')
parser.add_argument('pais')


class AgregarInmueble(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()

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
        except Inmueble.DoesNotExist as e:
            return {'message': e.args[0]}, 404
        return {'message': 'Inmueble con id: {} borrado exitosamente'.format(inmueble.id)}


class EditarInmueble(Resource):
    @jwt_required
    def put(self):
        data = parser.parse_args()

        edited_inmueble = service.persist_inmueble(nombre=data['nombre'],
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
                                                   inmueble_id=data['id'])

        if edited_inmueble:
            return edited_inmueble.to_dict()
        else:
            return {'message': 'El Inmueble no pudo ser editado'}, 500
