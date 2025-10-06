from app import create_app
import uuid
from datetime import datetime, timedelta, timezone
import requests
from flask import Flask, jsonify, request, session
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity
import os 
from apis.signup import signup_api, create_canteen_profile_api, login_api
from flask_jwt_extended import jwt_required, get_jwt_identity
from apis.no_login import all_canteens_api, fetch_canteen_info, get_canteen_review_ratings_api, get_canteen_menu_details_api
app = create_app()


@app.route('/check_jwt_status', methods=['POST'])
@jwt_required()
def check_jwt_status():
    jwt_data = get_jwt()
    exp_timestamp = jwt_data['exp']
    now = datetime.now(timezone.utc)
    exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    remaining = exp - now

    return jsonify({'message': 'JWT is valid.','remaining_time': str(remaining), 'status': 'success'}), 200

@app.route('/signup', methods=['POST'])
def signup_route(): 
    return signup_api()

@app.route("/create_canteen_profile", methods=["POST"])
def create_profile_route():
    return create_canteen_profile_api()

@app.route("/login", methods=["POST"])
def login_route():
    return login_api()
@app.route('/canteens', methods=['GET'])
def canteens_route():
    return all_canteens_api()

@app.route('/canteen_info', methods=['GET'])
def canteen_info_route():
    try:
        canteen_id = request.form.get('canteen_id')
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400
        return fetch_canteen_info(canteen_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500   
    
@app.route('/canteen_review_ratings', methods=['GET'])
def get_canteen_reviews_and_ratings_route():
    try:
        canteen_id = request.form.get('canteen_id')
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400
        return get_canteen_review_ratings_api(canteen_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500
    

@app.route('/canteen_menu_details', methods=['GET'])
def canteen_menu_details_route():
    try:
        canteen_id = request.form.get('canteen_id')
        if not canteen_id:
            return jsonify({"message": "canteen_id is required"}), 400
        return get_canteen_menu_details_api(canteen_id)
    except Exception as e:
        return jsonify({"message": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
