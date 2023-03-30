from werkzeug.security import check_password_hash, generate_password_hash
from .communicate_with_db import *
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import request, make_response
from datetime import datetime, timedelta
from .database import Event, User
from . import app
import json


def convert_time_to_object(time_to_format):
    return datetime.strptime(time_to_format, "%H:%M").time()


def convert_date_to_object(date_to_format):
    return datetime.strptime(date_to_format, "%Y-%m-%d").date()


def prepare_data_to_database(data):
    data = json.loads(data)
    data["user"] = get_jwt_identity()
    data["date"] = convert_date_to_object(data["date"])
    data["time"] = convert_time_to_object(data["time"])
    return data


@app.route("/create_event", methods=["POST"])
@jwt_required()
def create_event():
    if request.data:
        request_data = prepare_data_to_database(request.data)

        print(request_data)
        event = Event(**request_data)
        add_item_to_db(event)

        response = make_response({"msg": "success"})
        response.status_code = 200

        return response
    return make_response({"msg": "there's no data"}, 400)


@app.route("/get_events_by/<date>", methods=["GET"])
@jwt_required()
def get_events_by(date):
    current_user = get_jwt_identity()
    date = datetime.fromisoformat(date).date()
    data = get_events_for_current_user_by(date, current_user)
    response = make_response(data)
    return response


@app.route("/login", methods=["POST"])
def login():
    request_data = json.loads(request.data)
    user = get_user_by_nickname(request_data["nickname"])

    if user:
        is_password_correct = check_password_hash(user.password, request_data["password"])

        if is_password_correct:
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))

            response = make_response({"isLogged": True, "token": token})
            response.status_code = 200
            return response

        response = make_response({"isLogged": False})
        response.status_code = 400
        return response


@app.route("/signup", methods=["POST"])
def signup():
    request_data = json.loads(request.data)
    user = get_user_by_nickname(request_data["nickname"])

    if user:
        response = make_response({"isAddedToDB": False, "reason": "user exist"})
        response.status_code = 409
        return response

    password = generate_password_hash(request_data["password"])
    user = User(request_data["nickname"], request_data["email"], password)
    add_item_to_db(user)

    response = make_response({"isAddedToDB": True})
    response.status_code = 200
    return response


@app.route("/check_for_near_events")
def get_events():
    data = []
    for event in check_for_near_events():
        data.append(create_json_from(event))
    response = make_response(data)
    return response


@app.route("/get_user_email_by_id/<id>")
def get_email(id):
    response = make_response({"user_mail": get_user_email_by_id(id)})
    return response


@app.route("/delete_user_by/<email>")
def delete_user_by(email):
    try:
        delete_user_events_by_email(email)
        delete_user_by_email(email)
        resp_data = {"is_deleted": True}
        status = 200
    except:
        resp_data = {"is_deleted": False}
        status = 500

    response = make_response(resp_data)
    response.status_code = status
    return response


@app.route("/delete_event_by/<header>")
@jwt_required()
def delete_event_by(header):
    user = get_jwt_identity()
    try:
        delete_event_using(header, user)
        response_data = {"isDeleted": True}
        status_code = 200
    except:
        response_data = {"isDeleted": False}
        status_code = 409
    response = make_response(response_data, status_code)
    return response
