#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {"message": "Welcome to the Newsletter RESTful API"}
        return make_response(response_dict, 200)

api.add_resource(Home, '/')

class Newsletters(Resource):
    def get(self):
        newsletters = Newsletter.query.all()
        response_dict_list = [n.to_dict() for n in newsletters]
        return make_response(response_dict_list, 200)

    def post(self):
        # Support JSON payloads
        data = request.get_json()
        if not data or 'title' not in data or 'body' not in data:
            return make_response({"error": "Invalid data. Provide 'title' and 'body'."}, 400)

        new_record = Newsletter(
            title=data['title'],
            body=data['body'],
        )
        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()
        return make_response(response_dict, 201)

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):
    def get(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return make_response({"error": f"Newsletter with id {id} not found."}, 404)

        response_dict = record.to_dict()
        return make_response(response_dict, 200)

    def patch(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return make_response({"error": f"Newsletter with id {id} not found."}, 404)

        data = request.get_json()
        if not data:
            return make_response({"error": "No data provided for update."}, 400)

        for key, value in data.items():
            setattr(record, key, value)

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()
        return make_response(response_dict, 200)

    def delete(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return make_response({"error": f"Newsletter with id {id} not found."}, 404)

        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "Record successfully deleted"}
        return make_response(response_dict, 200)

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
