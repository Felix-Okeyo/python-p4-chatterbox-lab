from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.order_by(Message.created_at).all()

        all_messages_serialized = [message.to_dict()
                                   for message in all_messages]

        response = make_response(
            jsonify(all_messages_serialized),
            200
        )

        return response

    if request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data.get('body'),
            username=data.get('username')
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_serialized = new_message.to_dict()

        response_body = {
            "creation_successful": True,
            "body": new_message_serialized['body'],
            "username": new_message_serialized['username']
        }

        response = make_response(
            jsonify(response_body),
            201
        )

        return response

    return None
@app.route('/messages/<int:num>', methods=['PATCH', 'DELETE', 'GET'])
def messages_by_id(num):

    message = Message.query.filter_by(id=num).first()

    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])

        db.session.add(message)
        db.session.commit()

        message_serialized = message.to_dict()

        response = make_response(
            jsonify(message_serialized),
            200
        )

        return response

    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }

        response = make_response(
            jsonify(response_body),
            200
        )

        return response

    if request.method == 'GET':

        message_serialized = message.to_dict()

        response = make_response(
            jsonify(message_serialized),
            200
        )

        return response

    return None

if __name__ == '__main__':
    app.run(port=5555)
