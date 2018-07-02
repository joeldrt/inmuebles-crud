from flask_restful import Resource, reqparse
from data.inmuebles import Inmueble
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from services import inmueble_service as service

parser = reqparse.RequestParser()
parser.add_argument('nombre', help='This field cannot be blank', required=True)
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


class InmuebleAgregar(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()

        new_inmueble = service.create_inmueble(nombre=data['nombre'],
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
                                               pais=data['pais'])

        if new_inmueble:
            return {'message': 'Inmueble created with Id {}'.format(new_inmueble.id)}
        else:
            return {'message': 'Unable to save inmueble'}, 500


class ObtenerTodosLosInmuebles(Resource):
    @jwt_required
    def get(self):
        # user = get_jwt_identity()
        inmuebles = service.get_all_inmuebles()
        return {'inmuebles': inmuebles}
