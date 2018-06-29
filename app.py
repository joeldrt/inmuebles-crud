from bson import json_util, ObjectId
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'inmueblesgalatea'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/inmueblesgalatea'

mongo = PyMongo(app);


@app.route('/inmueble', methods=['GET'])
def obtener_todos_los_inmuebles():
    inmuebles = mongo.db.inmuebles
    output = []
    for inmueble in inmuebles.find():
        output.append({'_id': inmueble['_id'],
                       'nombre': inmueble['nombre'],
                       'metros-cuadrados': inmueble['metros-cuadrados'],
                       'ubicacion': inmueble['ubicacion']})
    output_sanitized = json.loads(json_util.dumps(output))
    return jsonify({'result': output_sanitized})


@app.route('/inmueble/', methods=['GET'])
def obtener_un_inmueble_por_nombre():
    nombre = request.args.get('nombre')
    inmuebles = mongo.db.inmuebles
    inmueble = inmuebles.find_one({'nombre': nombre})
    if inmueble:
        output = {'_id': inmueble['_id'],
                  'nombre': inmueble['nombre'],
                  'metros-cuadrados': inmueble['metros-cuadrados'],
                  'ubicacion': inmueble['ubicacion']}
    else:
        output = "No existe un inmueble con ese nombre"
    output_sanitized = json.loads(json_util.dumps(output))
    return jsonify({'result': output_sanitized})


@app.route('/inmueble', methods=['POST'])
def guardar_inmueble():
    inmuebles = mongo.db.inmuebles
    nombre = request.json['nombre']
    metros_cuadrados = request.json['metros-cuadrados']
    ubicacion = request.json['ubicacion']
    inmueble_id = inmuebles.insert({'nombre': nombre,
                                    'metros-cuadrados': metros_cuadrados,
                                    'ubicacion': ubicacion})
    inmueble_nuevo = inmuebles.find_one({'_id': inmueble_id})
    output = {'_id': inmueble_nuevo['_id'],
              'nombre': inmueble_nuevo['nombre'],
              'metros-cuadrados': inmueble_nuevo['metros-cuadrados'],
              'ubicacion': inmueble_nuevo['ubicacion']}
    output_sanitized = json.loads(json_util.dumps(output))
    return jsonify({'result': output_sanitized})


if __name__ == '__main__':
    app.run(debug=True)
