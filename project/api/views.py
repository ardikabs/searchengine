import json

from flask import Blueprint, request, jsonify, make_response
from project import engine

from project.miner import generator

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/search',methods=['GET'])
def search():
    query = request.args.get('q')
    if query != "":
        result = engine.search(query)
        response = {"status":"OK","result":result}
        return jsonify(response)
    else:
        return jsonify({"status":"OK","result":[]})
    
    
@api.route('/add-data/',methods=['POST'])
def add_data():
    missing = False
    data = request.json
    if missing:
        return error_response("Missing required fields: {}.",400)
    else:
        if generator.generate(data):
            return jsonify({"status":"OK","message":"Data berhasil ditambahkan"})
        else:
            return jsonify({"status":"ERROR"})
 


def error_response(message, status_code=400):
    resp = jsonify({'error': message})
    resp.status_code = status_code
    return resp