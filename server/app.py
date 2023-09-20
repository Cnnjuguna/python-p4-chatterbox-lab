from crypt import methods
from urllib import response
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False
app.json_encoder = None

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    # GET
    if request.method == "GET":
        messages = []
        for message in Message.query.all():
            message_dict = [message.to_dict() for message in messages]
            messages.append(message_dict)
            
        response = make_response(jsonify(messages), 200)
        
        return response
    
    # POST
    elif request.method == "POST":
        data = request.get_json()
        new_message = Message(
            body=data.get("body"),
            username=data.get("username"),
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        new_message_dict = new_message.to_dict()
        
        response = make_response(jsonify(new_message_dict), 201)
        
        
        return response
    

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message =  Message.query.filter_by(id=id).first()
    
    if message == None:
        response_body = {
            "message": "This record does not exist. Please try again."
        }
        
        response = make_response(jsonify(response_body), 404)
        
        return response
    
    else:
        if request.method == "PATCH":
        # Update the message's body
            data = request.get_json()
            message.body = data.get("body")
            db.session.commit()
                
            return jsonify(message.to_dict()), 200
        elif request.method == "DELETE":
            db.session.delete(message)
            db.session.commit()
            
            return "", 204 
            

if __name__ == '__main__':
    app.run(port=5555)
