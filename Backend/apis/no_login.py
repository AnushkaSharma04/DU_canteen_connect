from flask import Blueprint, request, jsonify, redirect, url_for
from app.models import add_user, check_user_exists, add_canteen_profile, get_user_by_phone, get_all_canteens_from_db, get_canteen_info_from_db, get_canteen_reviews_and_ratings_from_db, get_canteen_menu_from_db
import bcrypt
import logging
import jwt
from flask_jwt_extended import create_access_token
from datetime import timedelta

def all_canteens_api():
    try:
        canteens = get_all_canteens_from_db()

        if not canteens:
            return jsonify({"message": "No canteens found"}), 404

        return jsonify({
            "message": "Canteens fetched successfully",
            "canteens": canteens
        }), 200

    except Exception as e:
        logging.error(f"Error in canteen API: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def fetch_canteen_info(canteen_id):
    try:
        canteen_info = get_canteen_info_from_db(canteen_id)
        if not canteen_info:
            return jsonify({"message": "Canteen not found"}), 404
        return jsonify({
            "message": "Canteen info fetched successfully",
            "canteen_info": canteen_info
        }), 200 
    except Exception as e:
        logging.error(f"Error fetching canteen info: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
    
def get_canteen_review_ratings_api(canteen_id):
    try:
        data = get_canteen_reviews_and_ratings_from_db(canteen_id)

        if not data:
            return jsonify({"message": "Canteen not found or no reviews available"}), 404

        return jsonify({
            "message": "Canteen reviews and ratings fetched successfully",
            "data": data
        }), 200

    except Exception as e:
        logging.error(f"Error in canteen details API: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
    

def get_canteen_menu_details_api(canteen_id):
    try:    
        menu_data = get_canteen_menu_from_db(canteen_id)
        if not menu_data:
                return jsonify({"message": "Menu not found"}), 404

        return jsonify({
                "message": "Canteen menu fetched successfully",
                "data": menu_data
            }), 200

    except Exception as e:
        logging.error(f"Error fetching canteen menu details: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500