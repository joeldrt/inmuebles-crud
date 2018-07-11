from flask import send_from_directory
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from data.inmuebles import Inmueble
from run import app
import base64
import hashlib
import os
from services import inmueble_service

parser = reqparse.RequestParser()
parser.add_argument('filename', help='El campo no puede ser o estar vacío', required=True, type=str)
parser.add_argument('filetype', help='El campo no puede ser o estar vacío', required=True, type=str)
parser.add_argument('value', help='El campo no puede ser o estar vacío', required=True, type=str)
parser.add_argument('inmueble_id', help='El campo no puede ser o estar vacío', required=True, type=str)


@app.route('/foto/<string:inmueble_id>/<string:file_name>')
def send_html(inmueble_id, file_name):
    return send_from_directory('static/{}'.format(inmueble_id), file_name)


class UploadFoto(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        inmueble_id = data['inmueble_id']

        def switch_filetype(argument: str):
            switcher = {
                'image/gif': 'gif',
                'image/jpeg': 'jpg',
                'image/jpg': 'jpg',
                'image/png': 'png',
                'image/svg+xml': 'svg'
            }
            return switcher.get(argument, 'drf')

        def encryp_string(string_to_hash: str):
            sha_signature = hashlib.sha256(string_to_hash.encode()).hexdigest()
            return sha_signature

        extension = switch_filetype(data['filetype'])

        base64_data = str(data['value'])

        data_hash = encryp_string(base64_data)

        os.makedirs('static/{}'.format(inmueble_id), exist_ok=True)

        img = open('static/{}/{}.{}'.format(inmueble_id, data_hash, extension), 'wb')
        img.write(base64.decodebytes(base64_data.encode()))
        img.close()

        saved_file_name = '{}.{}'.format(data_hash, extension)

        inmueble = inmueble_service.get_inmueble_by_id(inmueble_id)
        if saved_file_name not in inmueble.fotos:
            inmueble.update(push__fotos=saved_file_name)

        return {'message': saved_file_name}


class DeleteFoto(Resource):
    @jwt_required
    def delete(self, inmueble_id, foto_path):
        try:
            inmueble = inmueble_service.get_inmueble_by_id(inmueble_id)
            listafotos = list(inmueble.fotos)
            listafotos.remove(foto_path)
            inmueble.fotos = listafotos
            inmueble.save()
        except Inmueble.DoesNotExist as e:
            return {'message': e.args[0]}, 404
        try:
            os.remove('static/{}/{}'.format(inmueble_id, foto_path))
        except OSError as ose:
            return {'message': ose.args[0]}, 500
        return {'message': 'foto: {} - DELETED'.format(foto_path)}
