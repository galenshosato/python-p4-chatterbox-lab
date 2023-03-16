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
        message_list = []
        for message in Message.query.order_by(Message.created_at).all():
            message_dict = message.to_dict()
            message_list.append(message_dict)
        
        reponse = make_response(
            jsonify(message_list),
            200
        )
    
        return reponse
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message()

        for field in data:
            setattr(new_message, field, data[field])
        
        db.session.add(new_message)
        db.session.commit()

        new_message_dict= new_message.to_dict()

        response = make_response(
            jsonify(new_message_dict),
            201
        )

        return response

@app.route('/messages/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def messages_by_id(id):
    if request.method == 'PATCH':
        message = Message.query.filter_by(id=id).first()
        data = request.get_json()

        for field in data:
            setattr(message, field, data[field])
        
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            jsonify(message_dict),
            200
        )

        return response
    
    elif request.method == 'DELETE':
        message = Message.query.filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()

        response_body = {
            'delete': "You have deleted this message...Don't be shady!"
        }

        response = make_response(
            response_body,
            200
        )

        return response
if __name__ == '__main__':
    app.run(port=5555)
