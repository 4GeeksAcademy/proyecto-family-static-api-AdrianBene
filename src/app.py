"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_api():
    # This is how you can use the Family datastructure by calling its methods
    response_body = jackson_family.get_all_members()
    if response_body is None:
        return 'fallo en la solicitud', 404

    return jsonify(response_body), 200


# PARA AÑADIR UN MIEMBRO A LA API
@app.route('/members', methods=['POST'])
def add_memberApi():
    response_body = jackson_family.get_all_members()

    if len(response_body) == 5:
        return "El cuerpo de la solicitud es null", 400

    request_body = request.get_json()
    # hacer validaciones de los datos aportados
    if request_body is None:
        return "El cuerpo de la solicitud es null", 400
    if 'first_name' not in request_body:
        return 'Debes especificar el name', 400
   
    if 'age' not in request_body:
        return 'Debes especificar el age', 400
    if 'lucky_numbers' not in request_body:
        return 'Debes especificar el lucky numbers', 400

    jackson_family.add_member(request_body)
    return jsonify(request_body), 200


# PARA ELIMINAR EN LA API

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_todo(id):
    if id is None:
        return 'El cuerpo de la solicitud es null', 400

    jackson_family.delete_member(id)
    return jsonify({"message": "El miembro ha sido borrado existosamente"}), 200



# BUSCAR MEMBER SEGUN EL ID
@app.route('/members/<int:id>', methods=['GET'])
def find_member(id):
    response_body = jackson_family.get_member(id)

    if id is None:
        return 'El cuerpo de la solicitud es null', 400

    return jsonify(response_body), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
