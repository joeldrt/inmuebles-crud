from flask import send_from_directory
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required)

from data.inmuebles import Inmueble
from run import app
import base64
import hashlib
import os
from services import inmueble_service

parser = reqparse.RequestParser()
parser.add_argument('inmueble_id', help='El campo no puede ser o estar vacío', required=True, type=str)
parser.add_argument('files', action='append', type=dict, required=True)

parser_update_image_list = reqparse.RequestParser()
parser_update_image_list.add_argument('inmueble_id', help='El campo no puede ser o estar vacío', required=True, type=str)
parser_update_image_list.add_argument('url_list', action='append', required=True)


@app.route('/foto/<string:inmueble_id>/<string:file_name>')
def send_html(inmueble_id, file_name):
    return send_from_directory('static/{}'.format(inmueble_id), file_name)


class UploadFotos(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        inmueble_id = data['inmueble_id']

        files = list(data['files'])
        if len(files) <= 0:
            return {'error', 'No files in request'}, 400
        try:
            inmueble = inmueble_service.get_inmueble_by_id(inmueble_id)
        except Inmueble.DoesNotExist as e:
            return {'error': e.args[0]}, 404

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

        added_images = [];

        for file_data in data['files']:
            extension = switch_filetype(file_data['filetype'])

            base64_data = str(file_data['value'])

            data_hash = encryp_string(base64_data)

            os.makedirs('static/{}'.format(inmueble_id), exist_ok=True)

            img = open('static/{}/{}.{}'.format(inmueble_id, data_hash, extension), 'wb')
            img.write(base64.decodebytes(base64_data.encode()))
            img.close()

            saved_file_name = '{}.{}'.format(data_hash, extension)

            if saved_file_name not in added_images:
                added_images.append(saved_file_name);

        all_images = list(inmueble.fotos)
        all_images.extend(added_images)
        inmueble.fotos = all_images;
        inmueble.save()

        return {'message': added_images}


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


class UpdateFotoList(Resource):
    @jwt_required
    def post(self):
        data = parser_update_image_list.parse_args()

        try:
            inmueble = inmueble_service.get_inmueble_by_id(data['inmueble_id'])
        except Inmueble.DoesNotExist as e:
            return {'message': e.args[0]}, 404

        inmueble.fotos = data['url_list']
        inmueble.save()
        return {'message': 'foto list for inmueble: {} - UPDATED'.format(inmueble.id)}
