
import json

from typing import Any
from flask import Flask, jsonify, request
from src.commands import get_command, set_command, set_expire_command, flush_command

app = Flask(__name__)


@app.route('/messages/<id>', methods=['GET'])
def get_message(id):
    try:
        ok, value =  get_command(int(id))
    except ValueError:
        return jsonify({"error":"invalid type %s, must be int" % id}), 403

    if ok:
        try:
            data = json.loads(value)
            if not isinstance(data, dict):
                data = {"error": "invalid data format %s" % value}
        except json.JSONDecodeError as e:
            data = {"error": str(e)}

        return jsonify(data)
    return jsonify({"error":"not found %s" % id}), 404

@app.route('/messages', methods=['POST'])
def set_message():
    if request.method == 'POST':
        content = request.get_json()
        print(content)
        data, status = validate_data(content)
        if status == 201:
            set_command(data['id'], json.dumps(data))
            set_expire_command(data['id'])
            return "created", 201
        return jsonify({"error":data}), status

    
@app.route('/messages/delete_all', methods=['DELETE'])
def delete_message():
    if request.method == 'DELETE':
        flush_command()
        return "deleted", 202



def validate_data(content:Any):
    if not content or not isinstance(content, dict):
        return "invalid data format", 403
    if "id" not in content or "message" not in content:
        return "id and message field must be provided", 403
    
    nid = content.get('id')
    message = content.get('message')
    if not isinstance(nid, int):
        return "id field must be int"
    if not isinstance(message, str):
        return "message field must be string"
    return content, 201

        
if __name__ == '__main__':
    app.run(debug=True)