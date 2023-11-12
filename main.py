from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
import psycopg2
from psycopg2 import extras
from bson import json_util


app = Flask(__name__)


def get_db_connection(database):
    databases = {
        "postgres": psycopg2.connect(host='localhost',
                            database='postgres',
                            port='5400',
                            user='postgres',
                            password='postgres'),
        "mongo": MongoClient('mongodb://localhost:27017/')
    }

    return databases.get(database, None)


@app.route('/eventos', methods=['POST'])
def eventos():
    if request.is_json:
        dados_json = request.get_json()

        client = get_db_connection('mongo')
        db_mongo = client['tcc']
        collection = db_mongo['eventos']

        try:
            collection.insert_one(dados_json)
            resposta = {'mensagem': 'JSON recebido com sucesso'}
        except Exception:
            return "deu merda"
        return jsonify(resposta)
    else:

        return jsonify({'erro': 'A solicitação não contém dados JSON'}), 400


@app.route("/eventos/<id_ordem>", methods=['GET'])
def eventos_get_by_ordem(id_ordem):

    client = get_db_connection('mongo')
    db_mongo = client['tcc']
    collection = db_mongo['eventos']

    query = {"ordem_servico": int(id_ordem)}

    result = collection.find(query)
    eventos = list(result)

    if not eventos:
        return make_response(jsonify({"erro": "no content"}), 204)

    return make_response(json_util.dumps(eventos), 200)


@app.route("/eventos", methods=['GET'])
def eventos_get():
    client = get_db_connection('mongo')
    db_mongo = client['tcc']
    collection = db_mongo['eventos']

    result = collection.find()
    eventos = list(result)

    if not eventos:
        return make_response(jsonify({"erro": "no content"}), 204)

    return make_response(json_util.dumps(eventos), 200)


@app.route('/operador/login', methods=['POST'])
def login():

    login = request.get_json()

    if not login.get('matricula', None) or not login.get('senha', None):
        return make_response(jsonify({'erro': 'matricula ou senha não fornecido'}), 404)

    conn = get_db_connection('postgres')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    sql = "select op.id_operador, op.nome, op.matricula from operador op where op.matricula = %s and op.senha= %s"
    cur.execute(sql, (login['matricula'], login['senha']))
    operador = cur.fetchone()

    if operador is None:
        return make_response(jsonify({'erro': 'matricula/senha incorreto'}), 404)

    cur.close()
    conn.close()
    return make_response(jsonify(operador), 200)

@app.route("/ordem_servico/<id_maquina>")
def ordem_servico_by_maquina(id_maquina):

    conn = get_db_connection('postgres')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    sql = "select * from ordem_servico as os where os.id_maquina_pk = %s and os.status='A'"

    cur.execute(sql, (int(id_maquina)),)
    maquina = cur.fetchone(sql)

    if maquina is None:
        return make_response(jsonify({'erro': 'maquina não encontrada'}), 404)

    cur.close()
    conn.close()
    return make_response(jsonify(maquina), 200)

app.debug = True
if __name__ == '__main__':
    app.run(debug=True)